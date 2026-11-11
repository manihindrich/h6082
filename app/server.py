#!/usr/bin/env python3
"""h6082 — a compact start page generated from markdown.

Each content/pages/*.md is one tab. In a file: `#` = (invisible) column,
`##` = framed block in the column, `###` = subheading inside a block.
Files and config are reloaded on change; open pages refresh via SSE.
The built-in editor (/edit/<file>) saves through /api/file.
UI language: [page] lang (en | cs); built-in pages live in content/system/<lang>/.
"""
import base64
import copy
import difflib
import hashlib
import hmac
import secrets
import email.utils
import html
import json
import logging
import os
import re
import socket
import ssl
import tempfile
import threading
import time
import tomllib
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlsplit

import defusedxml.ElementTree as SafeET
import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

APP = Path(__file__).resolve().parent
# Read-only mode for a public demo: no writes at all (editor, notes, tasks, theme, language,
# history), no live reload; content comes only from the image (app/defaults/), no volume needed.
READONLY = os.environ.get("H6082_READONLY", "").lower() in ("1", "true", "yes")
CONTENT = APP / "defaults" if READONLY else Path(os.environ.get("CONTENT_DIR", APP / "content"))
CFG_FILE = CONTENT / "config.toml"
PAGES = Path(os.environ.get("PAGES_DIR", CONTENT / "pages"))
STATIC = APP / "static"
PORT = int(os.environ.get("PORT", "8080"))
# Editor password (HTTP Basic) from the environment — set it in .env, never in config or md.
EDITOR_USER = os.environ.get("H6082_EDITOR_USER", "h6082")
EDITOR_PASSWORD = os.environ.get("H6082_EDITOR_PASSWORD", "")
# Extra hostnames for the deployment (comma separated), added to [api] allowed_hosts —
# a deployment can add its domain without touching the user's config.toml.
EXTRA_HOSTS = {h.strip().lower() for h in os.environ.get("H6082_ALLOWED_HOSTS", "").split(",") if h.strip()}
# CSP nonce placeholder: random per start, so md content cannot know it.
NONCE_PH = f"__nonce_{secrets.token_hex(8)}__"
SSE_SLOTS = threading.BoundedSemaphore(32)  # max. concurrent /events connections
RESERVED = {"static", "events", "healthz", "edit", "api", "history", "media"}
MEDIA = CONTENT / "media"                    # own images, served at /media/<file> (falls back to defaults)
MEDIA_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*\.(svg|png|jpe?g|webp|gif|avif|ico)$", re.I)
SYSTEM = CONTENT / "system"                  # user overrides of built-in pages: system/<lang>/<name>.md
DEFAULTS_DIR = APP / "defaults"              # shipped with the image: system pages, demo, media, config
DEFAULT_SYSTEM = DEFAULTS_DIR / "system"
SYSTEM_PAGES = {"h6082", "showcase", "docs"}  # + [page].about_tab; cannot be deleted
TRASH = CONTENT / ".trash"                   # "deleted" files (can be restored)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("h6082")

DEFAULTS = {
    "page": {
        "title": "home",
        "favicon": "◆",
        "lang": "en",
        "links_new_tab": True,
        "header": "",
        "about_tab": "h6082",
        "live_reload": True,
    },
    "tabs": {
        "order": [],
        "labels": {},
        "hidden": [],
        "show_single": False,
    },
    "editor": {
        "enabled": True,
        "autosave_ms": 800,
        "max_size_kb": 1024,
    },
    "api": {
        "allowed_hosts": ["127.0.0.1", "localhost"],
    },
    "checks": {
        "enabled": True,
        "interval_s": 60,
        "timeout_s": 4,
        "verify_tls": False,
    },
    "rss": {
        "enabled": True,
        "refresh_min": 15,
        "timeout_s": 8,
        "default_limit": 10,
    },
    "layout": {
        "columns_fixed": 0,
        "column_min_width": "240px",
        "page_max_width": "1600px",
        "padding": "14px",
        "gap": "12px",
        "block_gap": "10px",
        "block_padding": "6px 10px 8px",
        "radius": "6px",
        "h3_indent": "2px",
        "content_indent": "10px",
    },
    "font": {
        "family": '"JetBrains Mono", ui-monospace, Menlo, Consolas, monospace',
        "size": "13px",
        "line_height": "1.4",
        "block_title_transform": "none",
    },
    "colors": {
        "bg": "#1e1e1e",
        "panel": "#262626",
        "border": "#363636",
        "text": "#dcddde",
        "muted": "#999999",
        "accent": "#a882ff",
        "h2": "#a882ff",
        "h3": "#c6b6ff",
        "link": "#8a9cff",
        "link_hover": "#b5c0ff",
        "code_bg": "#2b2b2b",
        "code_fg": "#e0a96d",
        "mark_bg": "#6b5a1e",
        "quote_border": "#555555",
        "callout_note": "#448aff",
        "callout_tip": "#00bfa5",
        "callout_info": "#00b8d4",
        "callout_warning": "#ff9100",
        "callout_danger": "#ff5252",
    },
    "code": {
        "pygments_style": "monokai",
        "line_numbers": False,
        "wrap": True,
    },
    "theme": {
        "default": "obsidian",
        "auto_dark": "obsidian",
        "auto_light": "obsidian-light",
    },
    "themes": {},
    "history": {
        "enabled": True,
        "coalesce_min": 5,
        "max_versions": 50,
        "max_age_days": 90,
    },
    "system": {
        "enabled": True,
        "interval_s": 5,
        "disks": [{"label": "/", "path": "/host/disk/root"}],
        "temps": [],
    },
}

# ---------------------------------------------------------------- themes ----
# "obsidian" = [colors] + [code].pygments_style from the config; the others are presets.
# Keys as in [colors]; missing ones are taken from obsidian. scheme = dark | light.
_CALLOUTS_DARK = dict(callout_note="#448aff", callout_tip="#00bfa5", callout_info="#00b8d4",
                      callout_warning="#ff9100", callout_danger="#ff5252")
_CALLOUTS_LIGHT = dict(callout_note="#0969da", callout_tip="#1a7f37", callout_info="#0a7ea4",
                       callout_warning="#bf6a02", callout_danger="#cf222e")
THEME_PRESETS = {
    "nord": dict(scheme="dark", pygments_style="nord", label="nord",
                 bg="#2e3440", panel="#3b4252", border="#4c566a", text="#e5e9f0", muted="#a3abbd",
                 accent="#88c0d0", h2="#88c0d0", h3="#81a1c1", link="#8fbcbb", link_hover="#b4e0df",
                 code_bg="#2e3440", code_fg="#ebcb8b", mark_bg="#6b5f3a", quote_border="#4c566a",
                 callout_note="#5e81ac", callout_tip="#a3be8c", callout_info="#88c0d0",
                 callout_warning="#d08770", callout_danger="#bf616a"),
    "dracula": dict(scheme="dark", pygments_style="dracula", label="dracula",
                    bg="#282a36", panel="#2f3142", border="#44475a", text="#f8f8f2", muted="#9aa2cc",
                    accent="#bd93f9", h2="#bd93f9", h3="#ff79c6", link="#8be9fd", link_hover="#b9f3ff",
                    code_bg="#21222c", code_fg="#f1fa8c", mark_bg="#6b5f2a", quote_border="#6272a4",
                    callout_note="#6c8cff", callout_tip="#50fa7b", callout_info="#8be9fd",
                    callout_warning="#ffb86c", callout_danger="#ff5555"),
    "gruvbox-dark": dict(scheme="dark", pygments_style="gruvbox-dark", label="gruvbox",
                         bg="#282828", panel="#32302f", border="#504945", text="#ebdbb2", muted="#a89984",
                         accent="#fabd2f", h2="#fabd2f", h3="#8ec07c", link="#83a598", link_hover="#b0d0c0",
                         code_bg="#1d2021", code_fg="#fe8019", mark_bg="#79740e", quote_border="#665c54",
                         callout_note="#83a598", callout_tip="#b8bb26", callout_info="#8ec07c",
                         callout_warning="#fe8019", callout_danger="#fb4934"),
    "solarized-dark": dict(scheme="dark", pygments_style="solarized-dark", label="solarized",
                           bg="#002b36", panel="#073642", border="#1c4f5c", text="#c0cbcb", muted="#839496",
                           accent="#b58900", h2="#b58900", h3="#2aa198", link="#268bd2", link_hover="#62b2ef",
                           code_bg="#00212b", code_fg="#cb4b16", mark_bg="#5c4d00", quote_border="#586e75",
                           callout_note="#268bd2", callout_tip="#859900", callout_info="#2aa198",
                           callout_warning="#cb4b16", callout_danger="#dc322f"),
    "catppuccin-mocha": dict(scheme="dark", pygments_style="one-dark", label="catppuccin mocha",
                             bg="#1e1e2e", panel="#25253a", border="#45475a", text="#cdd6f4", muted="#9399b2",
                             accent="#cba6f7", h2="#cba6f7", h3="#f5c2e7", link="#89b4fa", link_hover="#b4d0fb",
                             code_bg="#181825", code_fg="#fab387", mark_bg="#5c5232", quote_border="#585b70",
                             callout_note="#89b4fa", callout_tip="#a6e3a1", callout_info="#94e2d5",
                             callout_warning="#fab387", callout_danger="#f38ba8"),
    "tokyo-night": dict(scheme="dark", pygments_style="one-dark", label="tokyo night",
                        bg="#1a1b26", panel="#1f2335", border="#3b4261", text="#c0caf5", muted="#8089b3",
                        accent="#7aa2f7", h2="#7aa2f7", h3="#bb9af7", link="#7dcfff", link_hover="#b4e6ff",
                        code_bg="#16161e", code_fg="#ff9e64", mark_bg="#4f4a2a", quote_border="#565f89",
                        callout_note="#7aa2f7", callout_tip="#9ece6a", callout_info="#7dcfff",
                        callout_warning="#e0af68", callout_danger="#f7768e"),
    "obsidian-light": dict(scheme="light", pygments_style="friendly", label="obsidian light",
                           bg="#ffffff", panel="#f6f6f6", border="#e0e0e0", text="#222222", muted="#6b6b6b",
                           accent="#7b4ff0", h2="#7b4ff0", h3="#5c4a99", link="#4a5fd6", link_hover="#2f3fb0",
                           code_bg="#eeeeee", code_fg="#b5541a", mark_bg="#fff2a8", quote_border="#c8c8c8",
                           **_CALLOUTS_LIGHT),
    "gruvbox-light": dict(scheme="light", pygments_style="gruvbox-light", label="gruvbox light",
                          bg="#fbf1c7", panel="#f2e5bc", border="#d5c4a1", text="#3c3836", muted="#7c6f64",
                          accent="#b57614", h2="#b57614", h3="#427b58", link="#076678", link_hover="#0b4f5c",
                          code_bg="#ebdbb2", code_fg="#af3a03", mark_bg="#fadb6e", quote_border="#bdae93",
                          callout_note="#076678", callout_tip="#79740e", callout_info="#427b58",
                          callout_warning="#af3a03", callout_danger="#9d0006"),
    "solarized-light": dict(scheme="light", pygments_style="solarized-light", label="solarized light",
                            bg="#fdf6e3", panel="#eee8d5", border="#d6cfb8", text="#3b4a4f", muted="#6f7f84",
                            accent="#b58900", h2="#9c7600", h3="#2aa198", link="#268bd2", link_hover="#1a6aa3",
                            code_bg="#e6dfc8", code_fg="#cb4b16", mark_bg="#f5e3a0", quote_border="#c9c2aa",
                            callout_note="#268bd2", callout_tip="#859900", callout_info="#2aa198",
                            callout_warning="#cb4b16", callout_danger="#dc322f"),
    "catppuccin-latte": dict(scheme="light", pygments_style="default", label="catppuccin latte",
                             bg="#eff1f5", panel="#e6e9ef", border="#ccd0da", text="#4c4f69", muted="#7c7f93",
                             accent="#8839ef", h2="#8839ef", h3="#179299", link="#1e66f5", link_hover="#0b4ac4",
                             code_bg="#dce0e8", code_fg="#e64553", mark_bg="#f9e2af", quote_border="#bcc0cc",
                             callout_note="#1e66f5", callout_tip="#40a02b", callout_info="#179299",
                             callout_warning="#df8e1d", callout_danger="#d20f39"),
    "paper": dict(scheme="light", pygments_style="default", label="paper",
                  bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#656d76",
                  accent="#0969da", h2="#0969da", h3="#8250df", link="#0969da", link_hover="#0550ae",
                  code_bg="#eff2f5", code_fg="#953800", mark_bg="#fff8c5", quote_border="#d0d7de",
                  **_CALLOUTS_LIGHT),
}

# Callout aliases (Obsidian/GitHub names) -> 5 base colours
CALLOUT_KIND = {
    "note": "note", "abstract": "note", "summary": "note", "tldr": "note", "quote": "note", "cite": "note", "example": "note",
    "tip": "tip", "hint": "tip", "important": "tip", "success": "tip", "check": "tip", "done": "tip",
    "info": "info", "todo": "info", "question": "info", "help": "info", "faq": "info",
    "warning": "warning", "caution": "warning", "attention": "warning",
    "danger": "danger", "error": "danger", "bug": "danger", "failure": "danger", "fail": "danger", "missing": "danger",
}

# ---------------------------------------------------------------- i18n ----
# UI strings. Keys prefixed `js_` are also passed to the browser scripts (as T.<key>).
# Placeholders in {braces} are filled by t(…, name=value) or in JS by .replace().

LANGS = ("en", "cs")
LANG_NAMES = {"en": "English", "cs": "Čeština"}

STRINGS = {
    "en": {
        "auto_system": "auto (system)",
        "dark": "dark",
        "light": "light",
        "st_tab": "tab",
        "st_right": "top right",
        "st_hidden": "hidden",
        "st_config": "configuration",
        "st_custom": "customised",
        "reset_default": "reset to the default version",
        "no_files": "no files",
        "newfile_placeholder": "name",
        "newfile_button": "create",
        "delete_file": "delete {name}",
        "rss_disabled": "RSS is disabled ([rss] enabled)",
        "rss_bad": "{{rss}}: missing or invalid feed URL",
        "loading_feed": "loading feed…",
        "loading": "loading…",
        "sys_disabled": "server stats are disabled ([system] enabled)",
        "email_nojs": "e-mail (enable JavaScript)",
        "history_disabled": "history is disabled ([history] enabled)",
        "editor_disabled_small": "the editor is disabled",
        "live_title": "live reload",
        "insecure_link": "unencrypted connection (http)",
        "note_aria": "note",
        "task_done_aria": "done",
        "task_delete": "delete task",
        "ed_view": "view ↗",
        "ed_history": "history",
        "ed_preview": "preview",
        "ed_reload": "reload from file",
        "ed_force": "overwrite",
        "ed_back": "back",
        "msg_no_pages": "There is no <code>.md</code> file in <code>content/pages/</code>.",
        "msg_no_tab": "Tab <code>{name}</code> does not exist.",
        "msg_editor_disabled": "The editor is disabled (<code>[editor] enabled = false</code>).",
        "msg_not_editable": "File <code>{name}</code> cannot be edited.",
        "msg_history_disabled": "History or the editor is disabled.",
        "msg_no_history": "File <code>{name}</code> has no history.",
        "h_no_change": "no change",
        "h_no_versions": "no versions yet — they appear with the first change of the file",
        "h_purge": "delete history",
        "h_versions": "Versions",
        "h_explain": "Each version is the state <b>before</b> a change. Edits within {min} min are merged.",
        "h_diff": "Diff",
        "h_pick": "Pick a version on the left.",
        "h_current": "current",
        "h_version": "version {v}",
        "h_restore": "restore this version",
        "h_restore_hint": "returns the file to its state before this change",
        "h_title": "history {name}",
        "h_editor": "✎ editor",
        "toml_err": "TOML error: {e} — the last valid config stays in effect",
        "err_editor_off": "the editor is disabled ([editor] enabled = false)",
        "err_host": "host {host!r} is not in [api] allowed_hosts",
        "err_origin": "Origin not allowed",
        "err_header": "missing X-H6082 header",
        "err_cl": "invalid Content-Length",
        "err_too_big": "the file is too large ([editor] max_size_kb)",
        "err_json": "a JSON object was expected",
        "err_sys_off": "server stats are disabled",
        "err_rss_off": "RSS is disabled",
        "err_feed_not_allowed": "this feed is not in any md file",
        "err_feed_load": "cannot load the feed ({e})",
        "err_widget_system": "system files cannot be edited from page widgets",
        "err_unknown_theme": "unknown theme",
        "err_unknown_lang": "unknown language",
        "err_config_edit": "config.toml cannot be edited safely — change it in the editor",
        "err_bad_request": "invalid request",
        "err_note_markers": "a note must not contain a {{note}} / {{/note}} line",
        "err_note_changed": "the note has changed meanwhile, reload the page",
        "err_tasks_changed": "the tasks have changed meanwhile, reloading the page",
        "err_empty_task": "empty task",
        "err_unknown_op": "unknown operation",
        "err_bad_task": "invalid task",
        "err_history_off": "history is disabled",
        "err_bad_file": "invalid file",
        "err_version_missing": "this version does not exist",
        "err_restore_failed": "restore failed: {e}",
        "err_unknown_endpoint": "unknown endpoint",
        "err_file_missing": "the file does not exist",
        "err_system_delete": "{name} is a system file and cannot be deleted",
        "err_delete_failed": "delete failed: {e}",
        "err_text_string": "text must be a string",
        "err_file_changed": "the file was changed elsewhere",
        "err_write_failed": "write failed: {e}",
        "err_checks_off": "checks are disabled",
        "err_bad_name": "invalid name (A-Z a-z 0-9 _ . -; reserved: static, events, healthz, edit, api, history, media, h6082, showcase, docs)",
        "err_exists": "{name}.md already exists",
        "err_host_421": "host {host!r} is not in [api] allowed_hosts",
        "new_file": "# Column 1\n\n## Block\n- [link](https://example.com)\n\n# Column 2\n\n## Another block\ntext\n",
        "js_locale": "en-GB",
        "js_theme_not_saved": "The theme was not saved: ",
        "js_lang_not_saved": "The language was not saved: ",
        "js_confirm_reset": "Reset {f} to the default version?\n\nYour changes are moved to content/.trash/.",
        "js_confirm_delete_file": "Delete {f}?\n\nThe file (and its translations) is moved to content/.trash/ and can be restored manually.",
        "js_server": "server: ",
        "js_unavailable": "unavailable",
        "js_history": "history: ",
        "js_no_changes": "no changes yet",
        "js_saved": "saved",
        "js_unsaved": "unsaved…",
        "js_error": "error ",
        "js_confirm_delete_task": "Delete the task “{t}”?",
        "js_new_task": "+ new task",
        "js_new_task_aria": "new task",
        "js_loaded": "loaded",
        "js_cannot_load": "cannot load: ",
        "js_saved_at": "saved ",
        "js_conflict": "the file was changed elsewhere — your changes are NOT saved",
        "js_cannot_save": "cannot save: ",
        "js_confirm_discard": "Discard unsaved changes and reload the file?",
        "js_confirm_overwrite": "Overwrite the file with your version?",
        "js_err": "error: ",
        "js_confirm_restore": "Restore {f} to the state from {w}?\n\nThe current state is saved to history first.",
        "js_confirm_purge": "Delete the whole history of {f}?\n\nThis cannot be undone.",
    },
    "cs": {
        "auto_system": "auto (systém)",
        "dark": "tmavé",
        "light": "světlé",
        "st_tab": "záložka",
        "st_right": "vpravo",
        "st_hidden": "skrytá",
        "st_config": "konfigurace",
        "st_custom": "upraveno",
        "reset_default": "vrátit výchozí verzi",
        "no_files": "žádné soubory",
        "newfile_placeholder": "název",
        "newfile_button": "vytvořit",
        "delete_file": "smazat {name}",
        "rss_disabled": "RSS je vypnuté ([rss] enabled)",
        "rss_bad": "{{rss}}: chybí nebo je neplatná URL feedu",
        "loading_feed": "načítám feed…",
        "loading": "načítám…",
        "sys_disabled": "výpis serveru je vypnutý ([system] enabled)",
        "email_nojs": "e-mail (zapni JavaScript)",
        "history_disabled": "historie je vypnutá ([history] enabled)",
        "editor_disabled_small": "editor je vypnutý",
        "live_title": "živé obnovení",
        "insecure_link": "nešifrované spojení (http)",
        "note_aria": "poznámka",
        "task_done_aria": "hotovo",
        "task_delete": "smazat úkol",
        "ed_view": "zobrazit ↗",
        "ed_history": "historie",
        "ed_preview": "náhled",
        "ed_reload": "načíst ze souboru",
        "ed_force": "přepsat",
        "ed_back": "zpět",
        "msg_no_pages": "Ve složce <code>content/pages/</code> není žádný <code>.md</code> soubor.",
        "msg_no_tab": "Záložka <code>{name}</code> neexistuje.",
        "msg_editor_disabled": "Editor je vypnutý (<code>[editor] enabled = false</code>).",
        "msg_not_editable": "Soubor <code>{name}</code> nejde upravovat.",
        "msg_history_disabled": "Historie nebo editor je vypnutý.",
        "msg_no_history": "Soubor <code>{name}</code> nemá historii.",
        "h_no_change": "beze změny",
        "h_no_versions": "zatím žádné verze — vzniknou při první změně souboru",
        "h_purge": "smazat historii",
        "h_versions": "Verze",
        "h_explain": "Každá verze je stav <b>před</b> změnou. Úpravy do {min} min se slučují.",
        "h_diff": "Rozdíl",
        "h_pick": "Vyber verzi vlevo.",
        "h_current": "aktuální",
        "h_version": "verze {v}",
        "h_restore": "obnovit tuto verzi",
        "h_restore_hint": "vrátí soubor do stavu před touto změnou",
        "h_title": "historie {name}",
        "h_editor": "✎ editor",
        "toml_err": "TOML chyba: {e} — platí poslední platný config",
        "err_editor_off": "editor je vypnutý ([editor] enabled = false)",
        "err_host": "host {host!r} není v [api] allowed_hosts",
        "err_origin": "nepovolený Origin",
        "err_header": "chybí hlavička X-H6082",
        "err_cl": "neplatná Content-Length",
        "err_too_big": "soubor je příliš velký ([editor] max_size_kb)",
        "err_json": "očekávám JSON objekt",
        "err_sys_off": "výpis serveru je vypnutý",
        "err_rss_off": "RSS je vypnuté",
        "err_feed_not_allowed": "feed není v žádném md souboru",
        "err_feed_load": "nelze načíst feed ({e})",
        "err_widget_system": "systémový soubor nejde upravovat z prvků stránky",
        "err_unknown_theme": "neznámý motiv",
        "err_unknown_lang": "neznámý jazyk",
        "err_config_edit": "config.toml nejde bezpečně upravit — změň ho v editoru",
        "err_bad_request": "neplatný požadavek",
        "err_note_markers": "poznámka nesmí obsahovat řádek {{note}} / {{/note}}",
        "err_note_changed": "poznámka se mezitím změnila, obnov stránku",
        "err_tasks_changed": "úkoly se mezitím změnily, obnovuji stránku",
        "err_empty_task": "prázdný úkol",
        "err_unknown_op": "neznámá operace",
        "err_bad_task": "neplatný úkol",
        "err_history_off": "historie je vypnutá",
        "err_bad_file": "neplatný soubor",
        "err_version_missing": "verze neexistuje",
        "err_restore_failed": "obnovení selhalo: {e}",
        "err_unknown_endpoint": "neznámý endpoint",
        "err_file_missing": "soubor neexistuje",
        "err_system_delete": "{name} je systémový soubor a nejde smazat",
        "err_delete_failed": "smazání selhalo: {e}",
        "err_text_string": "text musí být řetězec",
        "err_file_changed": "soubor byl změněn jinde",
        "err_write_failed": "zápis selhal: {e}",
        "err_checks_off": "kontroly jsou vypnuté",
        "err_bad_name": "neplatný název (A-Z a-z 0-9 _ . -; rezervované: static, events, healthz, edit, api, history, media, h6082, showcase, docs)",
        "err_exists": "{name}.md už existuje",
        "err_host_421": "host {host!r} není v [api] allowed_hosts",
        "new_file": "# Sloupec 1\n\n## Blok\n- [odkaz](https://example.com)\n\n# Sloupec 2\n\n## Další blok\ntext\n",
        "js_locale": "cs-CZ",
        "js_theme_not_saved": "Motiv se neuložil: ",
        "js_lang_not_saved": "Jazyk se neuložil: ",
        "js_confirm_reset": "Vrátit {f} na výchozí verzi?\n\nTvoje úpravy se přesunou do content/.trash/.",
        "js_confirm_delete_file": "Smazat {f}?\n\nSoubor (i jeho překlady) se přesune do content/.trash/ — jde vrátit ručně.",
        "js_server": "server: ",
        "js_unavailable": "nedostupné",
        "js_history": "historie: ",
        "js_no_changes": "zatím žádné změny",
        "js_saved": "uloženo",
        "js_unsaved": "neuloženo…",
        "js_error": "chyba ",
        "js_confirm_delete_task": "Smazat úkol „{t}“?",
        "js_new_task": "+ nový úkol",
        "js_new_task_aria": "nový úkol",
        "js_loaded": "načteno",
        "js_cannot_load": "nelze načíst: ",
        "js_saved_at": "uloženo ",
        "js_conflict": "soubor se mezitím změnil jinde — tvoje změny NEJSOU uložené",
        "js_cannot_save": "nelze uložit: ",
        "js_confirm_discard": "Zahodit neuložené změny a načíst soubor?",
        "js_confirm_overwrite": "Přepsat soubor tvou verzí?",
        "js_err": "chyba: ",
        "js_confirm_restore": "Obnovit {f} do stavu z {w}?\n\nSoučasný stav se nejdřív uloží do historie.",
        "js_confirm_purge": "Smazat celou historii souboru {f}?\n\nTo nejde vrátit.",
    },
}
assert STRINGS["en"].keys() == STRINGS["cs"].keys(), "i18n: en/cs keys differ"


def cur_lang(cfg):
    lang = cfg["page"]["lang"]
    return lang if lang in LANGS else "en"


def t(cfg, key, **kw):
    """Translated UI string for the configured language (falls back to English)."""
    s = STRINGS[cur_lang(cfg)].get(key) or STRINGS["en"][key]
    return s.format(**kw) if kw else s


def js_strings(cfg):
    """JS strings as a JSON object literal, safe to embed in <script>."""
    d = {k[3:]: v for k, v in STRINGS[cur_lang(cfg)].items() if k.startswith("js_")}
    d["readonly"] = READONLY
    return json.dumps(d, ensure_ascii=False).replace("</", "<\\/")


FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
CALLOUT_RE = re.compile(r"^>\s*\[!(\w+)\]([+-]?)\s*(.*)$")
COLUMN_RE = re.compile(r"^#(\s.*)?$")
LIST_RE = re.compile(r"^\s{0,3}(?:[-*+]|\d+[.)])\s")
TABLE_RE = re.compile(r"^\s{0,3}\|")
QUOTE_RE = re.compile(r"^\s{0,3}>")
ADMON_RE = re.compile(r"^(?:!!!|\?\?\?\+?)\s")
TAB_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
P_WRAP_RE = re.compile(r"^<p>(.*)</p>$", re.S)

def mtime(p):
    try:
        return p.stat().st_mtime_ns
    except OSError:
        return None


LANG_SUFFIX_RE = re.compile(r"^(.+)\.(" + "|".join(LANGS) + r")$")


def all_stems():
    """User tab names: pages/<name>.md and its translations pages/<name>.<lang>.md form one tab."""
    names = set()
    for p in PAGES.glob("*.md"):
        if TAB_RE.match(p.stem):
            m = LANG_SUFFIX_RE.match(p.stem)
            names.add(m.group(1) if m else p.stem)
    return sorted(names)


def page_variants(name):
    """All files of a user tab: the base file and its translations."""
    out = [PAGES / f"{name}.md"] + [PAGES / f"{name}.{lang}.md" for lang in LANGS]
    return [p for p in out if p.is_file()]


def page_path(cfg, name):
    """File to render for a tab in the current language (system pages from content/system/)."""
    lang = cur_lang(cfg)
    if name in SYSTEM_PAGES:
        cands = [SYSTEM / lang / f"{name}.md", DEFAULT_SYSTEM / lang / f"{name}.md",
                 SYSTEM / "en" / f"{name}.md", DEFAULT_SYSTEM / "en" / f"{name}.md"]
    else:
        cands = [PAGES / f"{name}.{lang}.md", PAGES / f"{name}.md"] + \
                [PAGES / f"{name}.{x}.md" for x in LANGS]
    return next((p for p in cands if p.is_file()), None)


def file_id(p):
    """Identifier used by the editor and APIs: `name.md`, `name.cs.md` or `system/<lang>/name.md`."""
    if p.parent.parent in (SYSTEM, DEFAULT_SYSTEM):
        return f"system/{p.parent.name}/{p.name}"
    return p.name


def system_files():
    """User overrides of built-in pages (only these are tracked by the history)."""
    return [p for lang in LANGS for p in sorted((SYSTEM / lang).glob("*.md")) if TAB_RE.match(p.stem)]


def default_of(p):
    """Shipped default for an override path content/system/<lang>/<name>.md (or None)."""
    if p.parent.parent == SYSTEM:
        d = DEFAULT_SYSTEM / p.parent.name / p.name
        return d if d.is_file() else None
    return None


def allowed_hosts(cfg):
    return {str(h).lower() for h in cfg["api"]["allowed_hosts"]} | EXTRA_HOSTS


def seed_content():
    """First start: create content/ folders, copy the default config and the demo tab.
    The demo is copied only once (marker content/.seeded), so a deleted demo never comes back
    and an update never overwrites anything in content/."""
    try:
        for d in (PAGES, MEDIA):
            d.mkdir(parents=True, exist_ok=True)
        if not CFG_FILE.exists():
            write_atomic(CFG_FILE, (DEFAULTS_DIR / "config.toml").read_text(encoding="utf-8"))
            log.info("seeded config.toml")
        marker = CONTENT / ".seeded"
        if not marker.exists():
            if not any(PAGES.glob("*.md")):
                for f in sorted((DEFAULTS_DIR / "pages").glob("*.md")):
                    write_atomic(PAGES / f.name, f.read_text(encoding="utf-8"))
                    log.info("seeded pages/%s", f.name)
            marker.write_text("h6082: initial content was copied; delete this file to copy the demo again\n")
    except OSError as e:
        log.warning("cannot seed content/ (%s) — continuing with defaults", e)


def content_signature():
    files = [CFG_FILE, *sorted(PAGES.glob("*.md")), *system_files()]
    return tuple((str(p), mtime(p)) for p in files)


# ---------------------------------------------------------------- config ----

def deep_merge(base, over, path=""):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k not in out:
            log.warning("config: unknown key %s%s ignored", path, k)
        elif isinstance(v, dict) and isinstance(out[k], dict) and out[k]:
            out[k] = deep_merge(out[k], v, f"{path}{k}.")
        else:
            out[k] = v
    return out


_cfg = {"mtime": object(), "cfg": DEFAULTS}


def readonly_overrides(cfg):
    """In read-only mode every feature that writes or reveals the server is switched off."""
    if not READONLY:
        return cfg
    cfg = copy.deepcopy(cfg)
    cfg["editor"]["enabled"] = False
    cfg["history"]["enabled"] = False
    cfg["system"]["enabled"] = False
    cfg["page"]["live_reload"] = False
    return cfg


def load_config():
    m = mtime(CFG_FILE)
    if m == _cfg["mtime"]:
        return _cfg["cfg"]
    _cfg["mtime"] = m
    if m is None:
        _cfg["cfg"] = readonly_overrides(DEFAULTS)
        return _cfg["cfg"]
    try:
        with CFG_FILE.open("rb") as f:
            _cfg["cfg"] = readonly_overrides(deep_merge(DEFAULTS, tomllib.load(f)))
        log.info("config loaded")
    except (tomllib.TOMLDecodeError, OSError) as e:
        log.warning("config.toml cannot be read (%s) — keeping the last valid one", e)
    return _cfg["cfg"]


def css_safe(v):
    """Config value for CSS / a style attribute: without characters that could escape the value."""
    return re.sub(r"[<>{};\"'\\\n\r]", "", str(v))


def css_vars(cfg):
    L, F, C = cfg["layout"], cfg["font"], cfg["colors"]
    n = int(L["columns_fixed"] or 0)
    grid = f"repeat({n}, minmax(0, 1fr))" if n > 0 else f"repeat(auto-fit, minmax({L['column_min_width']}, 1fr))"
    v = {
        "grid-cols": grid,
        "page-max": L["page_max_width"],
        "pad": L["padding"],
        "gap": L["gap"],
        "block-gap": L["block_gap"],
        "block-pad": L["block_padding"],
        "radius": L["radius"],
        "h3-indent": L["h3_indent"],
        "content-indent": L["content_indent"],
        "font-family": F["family"],
        "font-size": F["size"],
        "line-height": F["line_height"],
        "block-title-transform": F["block_title_transform"],
        "code-ws": "pre-wrap" if cfg["code"]["wrap"] else "pre",
    }
    return ":root{" + "".join(f"--{k}:{css_safe(val)};" for k, val in v.items()) + "}"


def pygments_css(style, prefix=".highlight"):
    if style not in set(get_all_styles()):
        log.warning("pygments_style %r does not exist — using monokai", style)
        style = "monokai"
    return HtmlFormatter(style=style).get_style_defs(prefix)


def themes(cfg):
    """{name: {scheme, label, pygments_style, <colours>}} ordered: dark, light."""
    base = dict(cfg["colors"], scheme="dark", label="obsidian", pygments_style=cfg["code"]["pygments_style"])
    out = {"obsidian": base}
    for name, t in list(THEME_PRESETS.items()) + list(cfg["themes"].items()):
        if not isinstance(t, dict) or not TAB_RE.match(name) or name == "auto":
            log.warning("theme %r ignored", name)
            continue
        out[name] = {**base, "label": name, **out.get(name, {}), **t}
    return dict(sorted(out.items(), key=lambda kv: (kv[1]["scheme"] == "light", kv[0] != "obsidian")))


def theme_names(cfg):
    return set(themes(cfg)) | {"auto"}


def _theme_block(sel, t):
    keys = [k for k in DEFAULTS["colors"]]
    body = "".join(f"--{k.replace('_', '-')}:{css_safe(t[k])};" for k in keys)
    return f"{sel}{{{body}--scheme:{'light' if t['scheme'] == 'light' else 'dark'};}}\n"


def themes_css(cfg):
    """CSS of all themes: :root[data-theme=…] + code highlighting; "auto" follows the OS."""
    T = themes(cfg)
    out = []
    for name, t in T.items():
        sel = f':root[data-theme="{name}"]'
        out.append(_theme_block(sel, t))
        out.append(pygments_css(t["pygments_style"], f"{sel} .highlight") + "\n")
    th = cfg["theme"]
    dark = T.get(th["auto_dark"], T["obsidian"])
    light = T.get(th["auto_light"], T.get("obsidian-light", T["obsidian"]))
    auto = ':root[data-theme="auto"]'
    out.append(_theme_block(auto, dark) + pygments_css(dark["pygments_style"], f"{auto} .highlight") + "\n")
    out.append("@media (prefers-color-scheme: light){" + _theme_block(auto, light)
               + pygments_css(light["pygments_style"], f"{auto} .highlight") + "}\n")
    return "".join(out)


def theme_swatches(cfg):
    """Shortcode {{theme}}: theme tiles (colour preview), a click switches the theme."""
    def tile(name, t, label):
        st = (f"--sw-bg:{css_safe(t['bg'])};--sw-panel:{css_safe(t['panel'])};"
              f"--sw-accent:{css_safe(t['accent'])};--sw-text:{css_safe(t['text'])};"
              f"--sw-link:{css_safe(t['link'])}")
        return (f'<button type="button" class="swatch" data-theme-set="{name}" style="{st}" title="{name}">'
                f'<span class="sw-dots"><i></i><i></i><i></i></span>{html.escape(label)}</button>')
    T = themes(cfg)
    th = cfg["theme"]
    dark = T.get(th["auto_dark"], T["obsidian"])
    light = T.get(th["auto_light"], dark)
    auto = (f'<button type="button" class="swatch auto" data-theme-set="auto" title="auto" '
            f'style="--sw-bg:{css_safe(dark["bg"])};--sw-panel:{css_safe(light["bg"])};'
            f'--sw-accent:{css_safe(dark["accent"])};--sw-text:{css_safe(dark["text"])};--sw-link:{css_safe(light["accent"])}">'
            f'<span class="sw-dots"><i></i><i></i><i></i></span>{t(cfg, "auto_system")}</button>')
    groups = []
    for scheme, label in (("dark", t(cfg, "dark")), ("light", t(cfg, "light"))):
        tiles = "".join(tile(n, t, str(t["label"])) for n, t in T.items() if t["scheme"] == scheme)
        if tiles:
            groups.append(f'<div class="sw-group"><small>{label}</small><div class="sw-grid">{tiles}</div></div>')
    return f'<div class="themes-pick">{auto}{"".join(groups)}</div>'


# Theme picker: sets data-theme at once and saves the choice to config.toml ([theme] default).
THEME_JS = """<script nonce="__NONCE__">
(() => {
  const T = __T__;
  const root = document.documentElement;
  const sync = () => document.querySelectorAll('.swatch[data-theme-set]').forEach((b) => {
    b.classList.toggle('active', b.dataset.themeSet === root.dataset.theme);
  });
  document.addEventListener('click', (e) => {
    const b = e.target.closest('.swatch[data-theme-set]');
    if (!b) return;
    const t = b.dataset.themeSet, prev = root.dataset.theme;
    root.dataset.theme = t;
    sync();
    if (T.readonly) {  // read-only: the choice lives only in this browser (cookie read by the server)
      document.cookie = 'h6082_theme=' + encodeURIComponent(t) + '; path=/; max-age=31536000; SameSite=Lax';
      return;
    }
    // save to config.toml ([theme] default) — applies to every browser
    fetch('/api/theme', {method: 'POST', headers: {'X-H6082': '1', 'Content-Type': 'application/json'},
      body: JSON.stringify({theme: t})}).then(async (r) => {
      if (r.ok) return;
      const j = await r.json().catch(() => ({}));
      root.dataset.theme = prev; sync();
      alert(T.theme_not_saved + (j.error || r.status));
    });
  });
  // language buttons ({{lang}}): saved to config.toml ([page] lang), then the page reloads
  document.addEventListener('click', async (e) => {
    const b = e.target.closest('.lang-btn[data-lang-set]');
    if (!b) return;
    if (T.readonly) {  // read-only: the choice lives only in this browser
      document.cookie = 'h6082_lang=' + encodeURIComponent(b.dataset.langSet) + '; path=/; max-age=31536000; SameSite=Lax';
      location.reload();
      return;
    }
    const r = await fetch('/api/lang', {method: 'POST', headers: {'X-H6082': '1', 'Content-Type': 'application/json'},
      body: JSON.stringify({lang: b.dataset.langSet})});
    if (r.ok) { location.reload(); return; }
    const j = await r.json().catch(() => ({}));
    alert(T.lang_not_saved + (j.error || r.status));
  });
  sync();
  window.h6082Theme = {sync};
})();
</script>"""


# ------------------------------------------------------------------ tabs ----

def list_tabs(cfg):
    """User tabs (left): [tabs].order first, then the rest alphabetically;
    without hidden tabs and without the about tab (that one is on the right)."""
    T = cfg["tabs"]
    stems = all_stems()
    excluded = set(T["hidden"]) | {cfg["page"]["about_tab"]}
    order = [s for s in T["order"] if s in stems]
    rest = [s for s in stems if s not in order]
    return [s for s in order + rest if s not in excluded]


def default_tab(cfg, tabs):
    """Home page `/`: the first user tab, otherwise the about tab, otherwise anything."""
    if tabs:
        return tabs[0]
    about = cfg["page"]["about_tab"]
    if about and page_path(cfg, about):
        return about
    stems = all_stems()
    return stems[0] if stems else None


def tab_label(cfg, name):
    """Tab label: a plain string, or a per-language table { en = "…", cs = "…" }."""
    label = cfg["tabs"]["labels"].get(name, name)
    if isinstance(label, dict):
        label = label.get(cur_lang(cfg)) or label.get("en") or next(iter(label.values()), name)
    return str(label)


# -------------------------------------------------------------- markdown ----

def iter_lines_with_fence(text):
    """Yields (line, is_outside_code_block)."""
    fence = None
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if m:
            tok = m.group(1)
            if fence is None:
                fence = tok
            elif tok[0] == fence[0] and len(tok) >= len(fence):
                fence = None
            yield line, False
            continue
        yield line, fence is None


def split_columns(text):
    """Splits text on `# …` lines (outside code blocks). Text before the first `#` = first column."""
    cols = [[]]
    for line, outside in iter_lines_with_fence(text):
        if outside and COLUMN_RE.match(line):
            cols.append([])
            continue
        cols[-1].append(line)
    texts = ["\n".join(c) for c in cols]
    return [t for i, t in enumerate(texts) if i > 0 or t.strip()]


def is_system(cfg, stem):
    return stem in SYSTEM_PAGES or stem == cfg["page"]["about_tab"]


def files_markdown(cfg, which="all"):
    """Shortcode {{files [system|user]}}: list of files with links to the editor.
    User tabs get a delete button (moves the file and its translations to content/.trash/)."""
    ed = cfg["editor"]["enabled"]
    tabs, about, hidden = list_tabs(cfg), cfg["page"]["about_tab"], set(cfg["tabs"]["hidden"])

    def state(name):
        return (t(cfg, "st_tab") if name in tabs else t(cfg, "st_right") if name == about
                else t(cfg, "st_hidden") if name in hidden else "")

    def edit_links(paths):
        return " · ".join(f"[{p.name}](/edit/{quote(file_id(p))})" if ed else f"`{p.name}`" for p in paths)

    lines = [""]
    if which in ("all", "user"):
        for name in all_stems():
            if is_system(cfg, name):
                continue
            dele = (f' <button class="del" data-file="{name}.md" title="{html.escape(t(cfg, "delete_file", name=name))}">✕</button>'
                    if ed else "")
            lines.append(f"- {edit_links(page_variants(name))} · [{html.escape(tab_label(cfg, name))} ↗](/{name}) "
                         f"<small>{state(name)}</small>{dele}")
    if which in ("all", "system"):
        for name in sorted(SYSTEM_PAGES):
            p = page_path(cfg, name)
            if p:
                custom = p.parent.parent == SYSTEM
                note = (" · " if state(name) else "") + t(cfg, "st_custom") if custom else ""
                reset = (f' <button class="del" data-file="{file_id(p)}" data-reset="1" '
                         f'title="{html.escape(t(cfg, "reset_default"))}">↺</button>' if custom and ed else "")
                lines.append(f"- {edit_links([p])} · [{html.escape(tab_label(cfg, name))} ↗](/{name}) "
                             f"<small>{state(name)}{note}</small>{reset}")
        cfg_link = "[config.toml](/edit/config.toml)" if ed else "`config.toml`"
        lines.append(f"- {cfg_link} <small>{t(cfg, 'st_config')}</small>")
    if len(lines) == 1:
        lines.append(f"<small>{t(cfg, 'no_files')}</small>")
    lines.append("")
    return lines


def newfile_html(cfg):
    return (f'<form class="newfile"><input name="n" placeholder="{t(cfg, "newfile_placeholder")}" autocomplete="off" '
            'pattern="[A-Za-z0-9][A-Za-z0-9_.\\-]*" required><span>.md</span>'
            f'<button type="submit">{t(cfg, "newfile_button")}</button></form>')


def lang_buttons(cfg):
    """Shortcode {{lang}}: language buttons; a click saves [page] lang to config.toml."""
    cur = cur_lang(cfg)
    btns = "".join(f'<button type="button" class="lang-btn{" active" if x == cur else ""}" data-lang-set="{x}">'
                   f'{LANG_NAMES[x]}</button>' for x in LANGS)
    return f'<div class="lang-pick">{btns}</div>'


SHORTCODE_RE = re.compile(r"^\{\{\s*(\w+)((?:\s+\S+)*)\s*\}\}$")


def rss_box(cfg, args):
    if not cfg["rss"]["enabled"]:
        return f"<small>{t(cfg, 'rss_disabled')}</small>"
    if not args or not valid_http(args[0]):
        return f"<small>{t(cfg, 'rss_bad')}</small>"
    limit = int(args[1]) if len(args) > 1 and args[1].isdigit() else int(cfg["rss"]["default_limit"])
    FEEDS.add(args[0])
    return (f'<div class="rss" data-feed="{html.escape(args[0])}" data-limit="{limit}">'
            f'<small>{t(cfg, "loading_feed")}</small></div>')


SYS_PARTS = ("cpu", "mem", "swap", "load", "temp", "uptime", "disk")


def sys_box(cfg, args):
    """{{sys [parts…] [demo]}} — `demo` = made-up values in the browser, no API call, no server data."""
    demo = "demo" in args
    if not demo and not cfg["system"]["enabled"]:
        return f"<small>{t(cfg, 'sys_disabled')}</small>"
    parts = [a for a in args if a in SYS_PARTS] or list(SYS_PARTS)
    d = ' data-demo="1"' if demo else ""
    return f'<div class="sys" data-sys="{" ".join(parts)}"{d}><small>{t(cfg, "loading")}</small></div>'


EMAIL_RE = re.compile(r"\{\{\s*email\s+([^\s{}@]+)\s+([^\s{}@]+)\s*\}\}")
INLINE_CODE_RE = re.compile(r"(`+).+?\1")


def email_html(m, cfg):
    """{{email user domain}} -> the address only encoded (base64 of the reversed text);
    JS in the browser builds the readable form and mailto:. Neither md nor HTML contains "user@domain"."""
    addr = f"{m.group(1)}@{m.group(2)}"
    enc = base64.b64encode(addr[::-1].encode()).decode()
    return f'<a class="email" href="#" data-e="{enc}">{t(cfg, "email_nojs")}</a>'


def inline_shortcodes(line, cfg):
    """Inline shortcodes ({{email …}}) outside `inline code`."""
    out, pos = [], 0
    for m in INLINE_CODE_RE.finditer(line):
        out.append(EMAIL_RE.sub(lambda e: email_html(e, cfg), line[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(EMAIL_RE.sub(lambda e: email_html(e, cfg), line[pos:]))
    return "".join(out)


def history_box(cfg, args):
    """{{history [file] [count] [demo]}} — `demo` = made-up changes, no real file names."""
    demo = "demo" in args
    if not demo and not cfg["history"]["enabled"]:
        return f"<small>{t(cfg, 'history_disabled')}</small>"
    fname = next((a for a in args if editable_path(a)), "")
    limit = next((a for a in args if a.isdigit()), "10")
    d = ' data-demo="1"' if demo else ""
    return (f'<div class="hist-box" data-file="{html.escape(fname)}" data-limit="{limit}"{d}>'
            f'<small>{t(cfg, "loading")}</small></div>')


def expand_shortcodes(cfg, text):
    """A line with a shortcode (outside code blocks) -> generated content:
    {{files [system|user]}}, {{newfile}}, {{lang}}, {{theme}}, {{rss URL [count]}}, {{sys …}}, {{history …}}."""
    out = []
    for line, outside in iter_lines_with_fence(text):
        s = line.strip()
        m = SHORTCODE_RE.match(s) if outside else None
        name, args = (m.group(1), m.group(2).split()) if m else (None, [])
        if name == "files":
            out.extend(files_markdown(cfg, args[0] if args and args[0] in ("system", "user") else "all"))
        elif name == "rss":
            out += ["", rss_box(cfg, args), ""]
        elif name == "theme":
            out += ["", theme_swatches(cfg), ""]
        elif name == "history":
            out += ["", history_box(cfg, args), ""]
        elif name == "sys":
            out += ["", sys_box(cfg, args), ""]
        elif name == "newfile":
            out += ["", newfile_html(cfg) if cfg["editor"]["enabled"]
                    else f"<small>{t(cfg, 'editor_disabled_small')}</small>", ""]
        elif name == "lang":
            out += ["", lang_buttons(cfg), ""]
        else:
            out.append(inline_shortcodes(line, cfg) if outside else line)
    return "\n".join(out)


def convert_callouts(text):
    """`> [!type][+-] Title` + following `>` lines -> div/details for md_in_html."""
    out, lines, i = [], list(iter_lines_with_fence(text)), 0
    while i < len(lines):
        line, outside = lines[i]
        m = CALLOUT_RE.match(line) if outside else None
        if not m:
            out.append(line)
            i += 1
            continue
        raw, fold, title = m.group(1).lower(), m.group(2), m.group(3).strip()
        kind = CALLOUT_KIND.get(raw, "note")
        body = []
        i += 1
        while i < len(lines) and lines[i][0].startswith(">"):
            body.append(re.sub(r"^> ?", "", lines[i][0]))
            i += 1
        tag, ttag = ("details", "summary") if fold else ("div", "div")
        opened = " open" if fold == "+" else ""
        out += [
            "",
            f'<{tag} class="callout callout-{kind} callout-raw-{raw}"{opened} markdown="1">',
            f'<{ttag} class="callout-title" markdown="span">{title or raw.capitalize()}</{ttag}>',
            "",
            *body,
            "",
            f"</{tag}>",
            "",
        ]
    return "\n".join(out)


LIST_ITEM_RE = re.compile(r"^( *)([-*+]|\d{1,9}[.)])( |$)")
QUOTE_PFX_RE = re.compile(r"^((?:> ?)*)")


def _reindent(body, shift):
    if shift >= 0:
        return " " * shift + body
    n = len(body) - len(body.lstrip(" "))
    return body[min(n, -shift):]


def nest_lists(text):
    """Nested lists by 2 spaces (like GitHub/Obsidian): list items are re-indented by their
    structure to 4 spaces per level, which Python-Markdown requires. An item indented by at
    least 2 more than the item above is its child; continuation lines move with their item."""
    out, stack, fence, shift, prev_pfx, blank = [], [], None, 0, "", True
    for line in text.split("\n"):
        pfx = QUOTE_PFX_RE.match(line).group(1)
        body = line[len(pfx):]
        if pfx != prev_pfx and not fence:
            stack, prev_pfx = [], pfx
        if fence:  # inside a fenced block: only move it with its list item
            out.append(pfx + _reindent(body, shift))
            m = FENCE_RE.match(body)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        if not body.strip():
            out.append(line)
            blank = True
            continue
        ind = len(body) - len(body.lstrip(" "))
        item = LIST_ITEM_RE.match(body)
        if item and (stack or ind < 4):
            while stack and stack[-1][0] > ind:
                stack.pop()
            content = len(item.group(0)) if item.group(3) else ind + len(item.group(2)) + 1
            if stack and ind < stack[-1][0] + 2:      # sibling
                new = stack[-1][1]
                stack[-1] = (ind, new, content)
            else:                                     # child (or the first item)
                new = stack[-1][1] + 4 if stack else 0
                stack.append((ind, new, content))
            shift = new - ind
            out.append(pfx + _reindent(body, shift))
        elif stack and ind > 0:                       # continuation of an item
            # to the content column of its item (4 past the item's new indent)
            shift = next((nw + 4 + max(0, ind - c) - ind for old, nw, c in reversed(stack) if old < ind), 0)
            out.append(pfx + _reindent(body, shift))
        else:
            if blank:
                stack = []
            shift = 0
            out.append(line)
        if m := FENCE_RE.match(body):
            fence = m.group(1)
        blank = False
    return "\n".join(out)


def _line_kind(line):
    if not line.strip():
        return "blank"
    for k, rx in (("list", LIST_RE), ("table", TABLE_RE), ("quote", QUOTE_RE), ("admon", ADMON_RE)):
        if rx.match(line):
            return k
    return "indent" if line[0] in " \t" else "text"


def separate_blocks(text):
    """Inserts a blank line before a list/table/quote/code block that directly follows text
    (like GitHub/Obsidian; Python-Markdown would not recognise them otherwise)."""
    out, prev, fence = [], "blank", None
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if fence:
            out.append(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence, prev = None, "text"
            continue
        if m:
            fence = m.group(1)
            if prev != "blank" and line[0] not in " \t":
                out.append("")
            out.append(line)
            continue
        k = _line_kind(line)
        if k in ("list", "table", "quote", "admon") and prev not in ("blank", k) \
                and not (k == "list" and prev == "indent"):
            out.append("")
        out.append(line)
        prev = k
    return "\n".join(out)


class _LinkTidy(Treeprocessor):
    """Bare URLs show without the scheme and trailing slash (https://a.cz/b/ -> a.cz/b);
    links to http:// get class="insecure" (a warning mark in CSS) and a title."""
    def __init__(self, md, title):
        super().__init__(md)
        self.title = title

    def run(self, root):
        for a in root.iter("a"):
            href = a.get("href") or ""
            low = href.lower()
            if not low.startswith(("http://", "https://")):
                continue
            if len(a) == 0 and a.text and a.text.strip() == href:
                short = href.split("://", 1)[1]
                a.text = markdown.util.AtomicString(short[:-1] if short.endswith("/") else short)
            if low.startswith("http://"):
                a.set("class", (a.get("class", "") + " insecure").strip())
                a.set("title", a.get("title") or self.title)


class _LinkTidyExt(Extension):
    def __init__(self, title):
        super().__init__()
        self.title = title

    def extendMarkdown(self, md):
        md.treeprocessors.register(_LinkTidy(md, self.title), "h6082_links", 1)


def make_md(cfg):
    return markdown.Markdown(
        extensions=[
            _LinkTidyExt(t(cfg, "insecure_link")),
            "extra",            # tabulky, abbr, def_list, footnotes, attr_list, md_in_html
            "sane_lists",
            "admonition",       # !!! note "Titulek"
            "pymdownx.details", # ??? note "Titulek"
            "pymdownx.superfences",
            "pymdownx.highlight",
            "pymdownx.inlinehilite",
            "pymdownx.magiclink",
            "pymdownx.tilde",
            "pymdownx.mark",
            "pymdownx.keys",
            "pymdownx.tasklist",
        ],
        extension_configs={
            "footnotes": {"UNIQUE_IDS": True},
            "pymdownx.highlight": {
                "use_pygments": True,
                "linenums": bool(cfg["code"]["line_numbers"]),
                "guess_lang": False,
            },
            "pymdownx.tilde": {"subscript": False},
            "pymdownx.tasklist": {"custom_checkbox": False},
        },
        output_format="html",
    )


def render_md(md, text):
    md.reset()
    return md.convert(separate_blocks(nest_lists(convert_callouts(text))))


def _split_heading(htm, level):
    """[(heading_html | None, content_html), …] split on top-level <hN>."""
    out = []
    for p in re.split(rf"(?=<h{level}[\s>])", htm):
        if p.startswith(f"<h{level}"):
            end = p.index(f"</h{level}>") + len(f"</h{level}>")
            out.append((p[:end], p[end:]))
        elif p.strip():
            out.append((None, p))
    return out


def _subsections(htm):
    parts = []
    for head, body in _split_heading(htm, 3):
        parts.append(f'<section class="s3">{head}<div class="b3">{body}</div></section>' if head else body)
    return "".join(parts)


def blocks(htm):
    """Each `##` (and content before the first `##`) -> a separate framed block."""
    out = []
    for head, body in _split_heading(htm, 2):
        inner = _subsections(body)
        body_html = f'<div class="block-body">{inner}</div>' if inner.strip() else ""
        out.append(f'<section class="block">{head or ""}{body_html}</section>')
    return "".join(out)


EXT_LINK_RE = re.compile(r'<a (?![^>]*\btarget=)([^>]*\bhref="https?://)')
A_TAG_RE = re.compile(r"<a\b[^>]*>")
CHECK_ATTR_RE = re.compile(r'\scheck="([^"]*)"')
CLASS_CHECK_RE = re.compile(r'\sclass="([^"]*\b)check(\b[^"]*)"')
HREF_RE = re.compile(r'\shref="([^"]*)"')

CHECK_TARGETS = set()   # targets /api/check may probe (only those found in md files)
FEEDS = set()           # feeds /api/rss may fetch (only those found in md files)


def valid_http(url):
    u = urlsplit(url)
    return u.scheme in ("http", "https") and bool(u.hostname)


def valid_target(t):
    u = urlsplit(t)
    if u.scheme == "tcp":
        try:
            return bool(u.hostname) and u.port is not None
        except ValueError:
            return False
    return valid_http(t)


def mark_checks(htm):
    """A link with {.check} (target = href) or {check="tcp://host:port"} -> data-check="target"."""
    def fix(m):
        tag, target = m.group(0), None
        cm = CHECK_ATTR_RE.search(tag)
        if cm:
            target = html.unescape(cm.group(1))
            tag = tag.replace(cm.group(0), "")
        ccm = CLASS_CHECK_RE.search(tag)
        if ccm:
            target = target or (html.unescape(h.group(1)) if (h := HREF_RE.search(tag)) else None)
            cls = (ccm.group(1) + ccm.group(2)).strip()
            tag = tag.replace(ccm.group(0), f' class="{cls}"' if cls else "")
        if not target or not valid_target(target):
            return tag
        CHECK_TARGETS.add(target)
        return tag[:-1] + f' data-check="{html.escape(target)}">'
    return A_TAG_RE.sub(fix, htm)


def postprocess(htm, cfg):
    if cfg["checks"]["enabled"]:
        htm = mark_checks(htm)
    if cfg["page"]["links_new_tab"]:
        htm = EXT_LINK_RE.sub(r'<a target="_blank" rel="noopener noreferrer" \1', htm)
    return htm


# ------------------------------------------------------------ javascript ----

# Live reload: EventSource on /events; on change the current page is fetched and
# <main>, CSS variables and title are swapped (no flicker, scroll position stays).
LIVE_JS = """<script nonce="__NONCE__">
(() => {
  const dot = () => document.querySelector('.live');
  const es = new EventSource('/events');
  es.onopen = () => dot()?.classList.add('on');
  es.onerror = () => dot()?.classList.remove('on');
  // while the user types into a note / new task, the reload waits until the field loses focus
  const holding = () => document.activeElement?.closest?.('[data-live-hold]');
  let pending = false;
  document.addEventListener('focusout', () => setTimeout(() => {
    if (pending && !holding()) { pending = false; refresh(); }
  }, 50));
  es.onmessage = () => { if (holding()) pending = true; else refresh(); };
  async function refresh() {
    try {
      const r = await fetch(location.href, {cache: 'no-store'});
      const d = new DOMParser().parseFromString(await r.text(), 'text/html');
      document.querySelector('main').replaceWith(d.querySelector('main'));
      document.documentElement.dataset.theme = d.documentElement.dataset.theme;
      document.getElementById('vars').replaceWith(d.getElementById('vars'));
      document.title = d.title;
      if (es.readyState === 1) dot()?.classList.add('on');
      const tl = document.getElementById('themes-css'), nl = d.getElementById('themes-css');
      if (tl && nl && tl.getAttribute('href') !== nl.getAttribute('href')) tl.replaceWith(nl);
      window.h6082?.init();
      window.h6082Theme?.sync();
    } catch (e) { console.warn('live reload', e); }
  }
  window.h6082Live = {refresh};
})();
</script>"""

# Interactive page widgets: new file, delete, service status, RSS, server stats, history,
# notes, tasks. Events are delegated to document (they survive <main> swaps by live reload);
# init() runs on load and after every live reload.
PAGE_JS = """<script nonce="__NONCE__">
window.h6082 = (() => {
  const T = __T__;
  const CHECK_S = __CHECK_S__;
  const api = async (url, opt = {}) => {
    const r = await fetch(url, {...opt, cache: 'no-store',
      headers: {'X-H6082': '1', 'Content-Type': 'application/json'}});
    return {ok: r.ok, status: r.status, j: await r.json().catch(() => ({}))};
  };

  document.addEventListener('submit', async (e) => {
    const f = e.target.closest('form.newfile');
    if (!f) return;
    e.preventDefault();
    const n = f.querySelector('input').value.trim().replace(/\\.md$/, '');
    const r = await api('/api/new', {method: 'POST', body: JSON.stringify({name: n})});
    if (r.ok) location.href = '/edit/' + encodeURIComponent(n) + '.md'; else alert(r.j.error || r.status);
  });

  document.addEventListener('click', async (e) => {
    const b = e.target.closest('button.del');
    if (!b) return;
    e.preventDefault();
    const f = b.dataset.file;
    const ask = b.dataset.reset ? T.confirm_reset : T.confirm_delete_file;
    if (!confirm(ask.replace('{f}', f))) return;
    const r = await api('/api/file?name=' + encodeURIComponent(f), {method: 'DELETE'});
    if (!r.ok) alert(r.j.error || r.status);
    else if (!window.EventSource || !document.querySelector('.live')) location.reload();
  });

  async function checks() {
    const els = [...document.querySelectorAll('[data-check]')];
    if (!els.length) return;
    const targets = [...new Set(els.map((e) => e.dataset.check))];
    const r = await api('/api/check', {method: 'POST', body: JSON.stringify({targets})}).catch(() => null);
    if (!r || !r.ok) return;
    for (const e of els) {
      const s = r.j[e.dataset.check];
      if (!s) continue;
      e.dataset.state = s.state;
      e.title = e.dataset.check + '\\n' + [s.state, s.status, s.ms != null ? s.ms + ' ms' : null, s.error]
        .filter((x) => x != null && x !== '').join(' · ');
    }
  }

  const ago = (ts) => {
    const m = Math.round((Date.now() / 1000 - ts) / 60);
    return m < 60 ? m + ' min' : m < 1440 ? Math.round(m / 60) + ' h' : Math.round(m / 1440) + ' d';
  };
  async function rss() {
    for (const box of document.querySelectorAll('.rss[data-feed]:not([data-done])')) {
      box.dataset.done = '1';
      const q = '?url=' + encodeURIComponent(box.dataset.feed) + '&limit=' + box.dataset.limit;
      const r = await api('/api/rss' + q).catch((e) => ({ok: false, j: {error: e.message}}));
      if (!r.ok) {
        const sm = document.createElement('small');
        sm.className = 'rss-err'; sm.textContent = 'RSS: ' + (r.j.error || r.status);
        box.replaceChildren(sm); continue;
      }
      const ul = document.createElement('ul');
      ul.className = 'rss-list';
      for (const it of r.j.items) {
        const li = document.createElement('li'), a = document.createElement('a');
        a.href = it.link; a.textContent = it.title; a.target = '_blank'; a.rel = 'noopener noreferrer';
        li.append(a);
        if (it.ts) { const t = document.createElement('small'); t.textContent = ' ' + ago(it.ts); li.append(t); }
        if (it.comments) {
          const c = document.createElement('a');
          c.href = it.comments; c.textContent = ' 💬'; c.className = 'rss-c'; c.target = '_blank'; c.rel = 'noopener noreferrer';
          li.append(c);
        }
        ul.append(li);
      }
      box.replaceChildren(ul);
    }
  }

  const SYS_S = __SYS_S__;
  const gib = (b) => b >= 1e12 ? (b / 1e12).toFixed(1) + ' TB' : b >= 1e9 ? (b / 1e9).toFixed(1) + ' GB' : (b / 1e6).toFixed(0) + ' MB';
  const dur = (s) => { const d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600), m = Math.floor(s % 3600 / 60);
    return (d ? d + ' d ' : '') + (d || h ? h + ' h ' : '') + m + ' min'; };
  const lvl = (p) => p >= 90 ? 'crit' : p >= 70 ? 'high' : '';
  function row(label, pct, text) {
    const r = document.createElement('div'); r.className = 'sys-row';
    const l = document.createElement('span'); l.className = 'sys-l'; l.textContent = label;
    r.append(l);
    if (pct != null) {
      const bar = document.createElement('span'); bar.className = 'sys-bar ' + lvl(pct);
      const fill = document.createElement('i'); fill.style.width = Math.min(100, Math.max(0, pct)) + '%';
      bar.append(fill); r.append(bar);
    }
    const v = document.createElement('span'); v.className = 'sys-v'; v.textContent = text;
    r.append(v);
    return r;
  }
  // made-up values for {{sys demo}} — demos and docs never show the real server's data
  const DEMO_SYS = () => ({
    cpu: {pct: 6 + Math.round(Math.random() * 12)},
    mem: {total: 8e9, used: 3.3e9 + Math.round(Math.random() * 3e8)},
    swap: {total: 2e9, used: 1.1e8},
    load: [0.42, 0.37, 0.31].map((x) => x + Math.random() * 0.1),
    uptime: 1123200 + Math.round(performance.now() / 1000),
    temp: [{label: 'CPU', c: 44 + Math.round(Math.random() * 5)}],
    disk: [{label: '/', total: 120e9, used: 48.2e9, pct: 40.2}, {label: 'data', total: 2e12, used: 1.31e12, pct: 65.5}],
  });
  async function sys() {
    const all = [...document.querySelectorAll('.sys[data-sys]')];
    if (!all.length || document.hidden) return;
    const demo = all.filter((b) => b.dataset.demo), real = all.filter((b) => !b.dataset.demo);
    if (demo.length) renderSys(demo, DEMO_SYS());
    if (!real.length) return;
    const r = await api('/api/sys').catch(() => null);
    if (!r || !r.ok) { real.forEach((b) => { b.textContent = T.server + ((r && r.j.error) || T.unavailable); }); return; }
    renderSys(real, r.j);
  }
  function renderSys(boxes, d) {
    for (const box of boxes) {
      const rows = [];
      for (const part of box.dataset.sys.split(' ')) {
        if (part === 'cpu' && d.cpu.pct != null) rows.push(row('CPU', d.cpu.pct, d.cpu.pct.toFixed(0) + ' %'));
        if (part === 'mem' && d.mem.total) { const p = 100 * d.mem.used / d.mem.total; rows.push(row('RAM', p, gib(d.mem.used) + ' / ' + gib(d.mem.total))); }
        if (part === 'swap' && d.swap.total) { const p = 100 * d.swap.used / d.swap.total; rows.push(row('swap', p, gib(d.swap.used) + ' / ' + gib(d.swap.total))); }
        if (part === 'load') rows.push(row('load', null, d.load.map((x) => x.toFixed(2)).join('  ')));
        if (part === 'temp') for (const t of d.temp) rows.push(row(t.label + ' °C', Math.min(100, t.c), t.c.toFixed(0) + ' °C'));
        if (part === 'uptime') rows.push(row('uptime', null, dur(d.uptime)));
        if (part === 'disk') for (const k of d.disk) rows.push(row(k.label, k.pct, gib(k.used) + ' / ' + gib(k.total)));
      }
      box.replaceChildren(...rows);
    }
  }

  function emails() {
    document.querySelectorAll('a.email[data-e]').forEach((a) => {
      const addr = [...atob(a.dataset.e)].reverse().join('');
      a.textContent = addr; a.href = 'mailto:' + addr; a.removeAttribute('data-e');
    });
  }

  const fmt = (ts) => new Date(ts * 1000).toLocaleString(T.locale,
    {day: 'numeric', month: 'numeric', hour: '2-digit', minute: '2-digit'});
  // made-up changes for {{history demo}}
  const DEMO_HIST = () => {
    const n = Date.now() / 1000;
    return [['nakup.md', 4 * 60, 2, 1], ['projekty.md', 2 * 3600, 5, 0], ['config.toml', 26 * 3600, 1, 1],
      ['cteni.md', 50 * 3600, 3, 2], ['nakup.md', 74 * 3600, 1, 4], ['recepty.md', 98 * 3600, 12, 0]]
      .map(([file, ago, added, removed]) => ({file, ts: n - ago, added, removed, demo: true}));
  };
  async function hist() {
    for (const box of document.querySelectorAll('.hist-box[data-limit]')) {
      let items;
      if (box.dataset.demo) items = DEMO_HIST().slice(0, +box.dataset.limit);
      else {
        const q = '?limit=' + box.dataset.limit + (box.dataset.file ? '&file=' + encodeURIComponent(box.dataset.file) : '');
        const r = await api('/api/history' + q).catch(() => null);
        if (!r || !r.ok) { box.textContent = T.history + ((r && r.j.error) || T.unavailable); continue; }
        items = r.j.items;
      }
      if (!items.length) { const sm = document.createElement('small'); sm.textContent = T.no_changes; box.replaceChildren(sm); continue; }
      const ul = document.createElement('ul'); ul.className = 'hist-list';
      for (const it of items) {
        const li = document.createElement('li');
        const t = document.createElement('small'); t.textContent = fmt(it.ts) + ' ';
        const a = document.createElement(it.demo ? 'span' : 'a');
        if (!it.demo) a.href = '/history/' + encodeURIComponent(it.file) + '?v=' + encodeURIComponent(it.v);
        a.textContent = it.file;
        const add = document.createElement('span'); add.className = 'h-add'; add.textContent = ' +' + it.added;
        const del = document.createElement('span'); del.className = 'h-del'; del.textContent = ' −' + it.removed;
        li.append(t, a, add, del); ul.append(li);
      }
      box.replaceChildren(ul);
    }
    document.querySelectorAll('time[data-ts]').forEach((t) => { t.textContent = fmt(+t.dataset.ts); });
  }

  // ---- notes: the textarea grows downwards and saves itself
  const grow = (ta) => { ta.style.height = 'auto'; ta.style.height = (ta.scrollHeight + 2) + 'px'; };
  const noteSt = (ta, t, c) => { const s = ta.parentElement.querySelector('.note-st'); if (s) { s.textContent = t; s.className = 'note-st ' + (c || ''); } };
  async function saveNote(ta) {
    if (ta._saving) { ta._again = true; return; }
    ta._saving = true;
    const text = ta.value, orig = ta.dataset.orig ?? ta.defaultValue;
    const r = await api('/api/note', {method: 'POST',
      body: JSON.stringify({file: ta.dataset.file, i: +ta.dataset.i, orig, text})}).catch((e) => ({ok: false, j: {error: e.message}}));
    if (r.ok) { ta.dataset.orig = text; noteSt(ta, T.saved, 'ok'); }
    else noteSt(ta, r.j.error || (T.error + r.status), 'err');
    ta._saving = false;
    if (ta._again) { ta._again = false; if (ta.value !== text && r.ok) saveNote(ta); }
  }
  document.addEventListener('input', (e) => {
    const ta = e.target.closest('textarea.note-area[data-file]');
    if (!ta) return;
    grow(ta); noteSt(ta, T.unsaved);
    clearTimeout(ta._t); ta._t = setTimeout(() => saveNote(ta), 800);
  });

  // ---- tasks: toggle, delete, add
  const grid = () => document.querySelector('.grid[data-tasks-sig]');
  async function taskOp(body, refresh) {
    const g = grid();
    if (!g) return false;
    const r = await api('/api/tasks', {method: 'POST',
      body: JSON.stringify({...body, file: g.dataset.file, sig: g.dataset.tasksSig})});
    if (!r.ok) {
      if (r.status === 409) (window.h6082Live?.refresh || (() => location.reload()))();
      else alert(r.j.error || r.status);
      return false;
    }
    g.dataset.tasksSig = r.j.sig;
    if (refresh) (window.h6082Live?.refresh || (() => location.reload()))();
    return true;
  }
  document.addEventListener('change', async (e) => {
    const cb = e.target.closest('input.task');
    if (!cb) return;
    if (!(await taskOp({op: 'toggle', i: +cb.dataset.i}, false))) cb.checked = !cb.checked;
  });
  document.addEventListener('click', (e) => {
    const b = e.target.closest('button.task-del');
    if (!b) return;
    const li = b.closest('li');
    const label = li ? li.textContent.replace('✕', '').trim() : '';
    if (confirm(T.confirm_delete_task.replace('{t}', label.slice(0, 80)))) taskOp({op: 'delete', i: +b.dataset.i}, true);
  });
  document.addEventListener('submit', async (e) => {
    const f = e.target.closest('form.task-add');
    if (!f) return;
    e.preventDefault();
    const inp = f.querySelector('input'), text = inp.value.trim();
    if (!text) return;
    inp.blur();
    if (await taskOp({op: 'add', first: +f.dataset.first, last: +f.dataset.last, text}, true)) inp.value = '';
  });
  function tasksUi() {
    const g = grid();
    if (!g) return;
    for (const ul of g.querySelectorAll('.task-list')) {
      if (ul.parentElement.closest('.task-list') || ul.querySelector(':scope > li.task-add')) continue;
      const idx = [...ul.querySelectorAll('input.task')].map((x) => +x.dataset.i);
      if (!idx.length) continue;
      const li = document.createElement('li'); li.className = 'task-add';
      const f = document.createElement('form'); f.className = 'task-add';
      f.dataset.first = Math.min(...idx); f.dataset.last = Math.max(...idx);
      const inp = document.createElement('input');
      inp.placeholder = T.new_task; inp.setAttribute('data-live-hold', ''); inp.setAttribute('aria-label', T.new_task_aria);
      f.append(inp); li.append(f); ul.append(li);
    }
  }

  function init() {
    emails(); checks(); rss(); sys(); hist(); tasksUi();
    document.querySelectorAll('textarea.note-area').forEach(grow);
  }
  if (CHECK_S > 0) setInterval(checks, CHECK_S * 1000);
  if (SYS_S > 0) setInterval(sys, SYS_S * 1000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) sys(); });
  init();
  return {init};
})();
</script>"""

# Smart typing in the editor textarea: auto-paired brackets and quotes, list / quote
# continuation on Enter, ``` fences, Tab / Shift+Tab indentation. Edits go through
# execCommand('insertText') so Ctrl+Z keeps working. Markdown rules only for .md files.
SMART_JS = r"""
function smartEditor(ta, MD) {
  const PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>', '"': '"', "'": "'", '`': '`'};
  const CLOSERS = new Set(Object.values(PAIRS));
  const FENCE = /^[ \t]*(```|~~~)/;
  let ltAuto = -1;  // position of a '>' we inserted right after '<'

  // replace [from, to) with text, then select from+a .. from+b
  function put(text, from, to, a, b = a) {
    ta.focus();
    ta.setSelectionRange(from, to);
    const ok = text ? document.execCommand('insertText', false, text)
                    : (from === to || document.execCommand('delete'));
    if (!ok) {
      ta.setRangeText(text, from, to, 'end');
      ta.dispatchEvent(new Event('input', {bubbles: true}));
    }
    ta.setSelectionRange(from + a, from + b);
  }
  const lineStart = (v, p) => v.lastIndexOf('\n', p - 1) + 1;
  const lineEnd = (v, p) => { const i = v.indexOf('\n', p); return i < 0 ? v.length : i; };
  const fencesIn = (text) => text.split('\n').filter((l) => FENCE.test(l)).length;
  const LIST = /^((?:[ \t]*>[ \t]?)*[ \t]*)([-*+]|(\d{1,9})([.)]))([ \t]+)(\[[ xX]\][ \t]+)?/;
  const QUOTE = /^[ \t]*(?:>[ \t]?)+/;

  function enter(v, s, en, ls) {
    const before = v.slice(ls, s), after = v.slice(en, lineEnd(v, en));
    const inCode = MD && fencesIn(v.slice(0, ls)) % 2 === 1;
    if (MD && !inCode) {
      const f = /^([ \t]*)(`{3,}|~{3,})[^`]*$/.exec(before);
      if (f && s === en && !after.trim() && fencesIn(v.slice(lineEnd(v, s))) % 2 === 0) {
        const mid = '\n' + f[1];
        put(mid + '\n' + f[1] + f[2], s, en, mid.length);
        return true;
      }
      const m = LIST.exec(before);
      if (m) {
        if (before.length === m[0].length && !after.trim()) { put('', ls, lineEnd(v, en), 0); return true; }
        const mark = m[3] ? (Number(m[3]) + 1) + m[4] : m[2];
        const text = '\n' + m[1] + mark + m[5] + (m[6] ? '[ ] ' : '');
        put(text, s, en, text.length);
        return true;
      }
      const q = QUOTE.exec(before);
      if (q) {
        if (!before.slice(q[0].length).trim() && !after.trim()) { put('', ls, lineEnd(v, en), 0); return true; }
        const text = '\n' + q[0].replace(/>$/, '> ');
        put(text, s, en, text.length);
        return true;
      }
    }
    const ind = /^[ \t]*/.exec(before)[0];
    if (!ind) return false;
    put('\n' + ind, s, en, 1 + ind.length);
    return true;
  }

  function tab(v, s, en, ls, back) {
    const unit = MD ? '  ' : '    ';
    if (s !== en && v.slice(s, en).includes('\n')) {  // block indent / outdent of whole lines
      const le = lineEnd(v, en > s && v[en - 1] === '\n' ? en - 1 : en);
      const lines = v.slice(ls, le).split('\n');
      const out = lines.map((l) => back ? l.replace(new RegExp('^(\\t| {1,' + unit.length + '})'), '') : unit + l).join('\n');
      put(out, ls, le, 0, out.length);
      return;
    }
    const m = MD ? LIST.exec(v.slice(ls, lineEnd(v, ls))) : null;
    if (back) {
      const width = m ? (m[2] + m[5]).length : 4;
      const lead = /^ */.exec(v.slice(ls))[0].length;
      const n = Math.min(width, lead);
      if (!n) return;
      put('', ls, ls + n, 0);
      ta.setSelectionRange(Math.max(ls, s - n), Math.max(ls, en - n));
    } else if (m && s === en) {
      const ind = ' '.repeat((m[2] + m[5]).length), at = ls + m[1].length;
      put(ind, at, at, 0);
      ta.setSelectionRange(s + ind.length, s + ind.length);
    } else {
      put('    ', s, en, 4);
    }
  }

  ta.addEventListener('keydown', (e) => {
    if (e.isComposing || e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
    const v = ta.value, s = ta.selectionStart, en = ta.selectionEnd, k = e.key;
    const ls = lineStart(v, s), prev = v[s - 1] || '', next = v[en] || '';
    const lt = ltAuto; ltAuto = -1;

    if (k === 'Enter') {
      if (!e.shiftKey && enter(v, s, en, ls)) e.preventDefault();
      return;
    }
    if (k === 'Tab') { e.preventDefault(); tab(v, s, en, ls, e.shiftKey); return; }
    if (k === 'Backspace') {
      if (s === en && PAIRS[prev] && PAIRS[prev] === next) { e.preventDefault(); put('', s - 1, s + 1, 0); }
      return;
    }
    if (k.length !== 1) return;
    // "a < b", "<=": drop the '>' we paired with '<' a moment ago
    if (s === en && lt === s && prev === '<' && next === '>' && (k === ' ' || k === '=')) {
      e.preventDefault(); put('<' + k, s - 1, s + 1, 2); return;
    }
    // typing a closer that is already there just steps over it
    if (s === en && CLOSERS.has(k) && next === k) { e.preventDefault(); ta.setSelectionRange(s + 1, s + 1); return; }
    const c = PAIRS[k];
    if (!c) return;
    if (s !== en) {  // wrap the selection
      e.preventDefault(); put(k + v.slice(s, en) + c, s, en, 1, 1 + en - s); return;
    }
    if (c === k && /[\p{L}\p{N}`]/u.test(prev)) return;    // don't, it's, ```
    if (next && !/[\s)\]}>.,;:!?'"`*_~]/.test(next)) return;  // right before a word
    e.preventDefault();
    put(k + c, s, s, 1);
    if (k === '<') ltAuto = s + 1;
  });
}
"""

EDITOR_JS = """<script nonce="__NONCE__">
__SMART__
(() => {
  const T = __T__;
  const NAME = __NAME__, DELAY = __DELAY__;
  const ta = document.getElementById('src'), st = document.getElementById('status');
  const cf = document.getElementById('conflict');
  const H = {'X-H6082': '1'};
  const url = '/api/file?name=' + encodeURIComponent(NAME);
  let mtime = null, timer = null, saving = false, again = false, blocked = false, saved = null;
  const set = (t, c) => { st.textContent = t; st.className = 'st ' + (c || ''); };
  const dirty = () => saved !== null && ta.value !== saved;

  async function load() {
    try {
      const r = await fetch(url, {headers: H, cache: 'no-store'});
      const j = await r.json();
      if (!r.ok) { set(T.err + j.error, 'err'); ta.disabled = true; return; }
      ta.value = saved = j.text; mtime = j.mtime; blocked = false; cf.hidden = true; ta.disabled = false;
      set(j.warning ? '⚠ ' + j.warning : T.loaded, j.warning ? 'warn' : 'ok');
      ta.focus();
    } catch (e) { set(T.cannot_load + e.message, 'err'); }
  }

  async function save(force) {
    clearTimeout(timer);
    if (blocked && !force) return;
    if (saving) { again = true; return; }
    if (!dirty() && !force) return;
    saving = true; again = false;
    const text = ta.value;
    try {
      const r = await fetch(url, {method: 'PUT', headers: {...H, 'Content-Type': 'application/json'},
        body: JSON.stringify({text, mtime: force ? null : mtime})});
      const j = await r.json();
      if (r.ok) {
        mtime = j.mtime; saved = text; blocked = false; cf.hidden = true;
        set(j.warning ? '⚠ ' + j.warning : T.saved_at + new Date().toLocaleTimeString(T.locale), j.warning ? 'warn' : 'ok');
      } else if (r.status === 409) {
        blocked = true; cf.hidden = false;
        set(T.conflict, 'err');
      } else set(T.err + (j.error || r.status), 'err');
    } catch (e) { set(T.cannot_save + e.message, 'err'); }
    saving = false;
    if (again || (!blocked && dirty())) save();
  }

  ta.addEventListener('input', () => {
    if (!blocked) set(T.unsaved, 'pending');
    clearTimeout(timer); timer = setTimeout(save, DELAY);
  });
  ta.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') { e.preventDefault(); save(); }
  });
  smartEditor(ta, /\\.md$/i.test(NAME));
  document.getElementById('reload').onclick = () => { if (!dirty() || confirm(T.confirm_discard)) load(); };
  document.getElementById('force').onclick = () => { if (confirm(T.confirm_overwrite)) save(true); };
  window.addEventListener('beforeunload', (e) => { if (dirty()) { save(); e.preventDefault(); e.returnValue = ''; } });
  load();
})();
</script>"""


# ------------------------------------------------------------------ html ----

def favicon(cfg):
    fav = html.escape(str(cfg["page"]["favicon"]))
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{fav}</text></svg>"
    return "data:image/svg+xml," + quote(svg)


def page(cfg, title, body, scripts="", body_class=""):
    scripts = scripts.replace("__NONCE__", NONCE_PH).replace("__T__", js_strings(cfg))
    theme_js = THEME_JS.replace("__NONCE__", NONCE_PH).replace("__T__", js_strings(cfg))
    return f"""<!doctype html>
<html lang="{cur_lang(cfg)}" data-theme="__THEME__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="icon" href="{favicon(cfg)}">
<link rel="stylesheet" href="/static/style.css?v={mtime(STATIC / 'style.css')}">
<link rel="stylesheet" id="themes-css" href="/themes.css?v={_cfg['mtime']}">
<style id="vars">{css_vars(cfg)}</style>
</head>
<body class="{body_class}">
<main>
{body}
</main>
{scripts}
{theme_js}
</body>
</html>"""


def tab_bar(cfg, tabs, active, live=True):
    """Top bar: header | user tabs … current hidden tab | about | live."""
    def link(name, extra=""):
        on = name == active
        cls = "tab" + extra + (" active" if on else "")
        cur = ' aria-current="page"' if on else ""
        return f'<a class="{cls}"{cur} href="/{quote(name)}">{html.escape(tab_label(cfg, name))}</a>'

    left, right = [], []
    header = str(cfg["page"]["header"]).strip()
    if header:
        brand = P_WRAP_RE.sub(r"\1", make_md(cfg).convert(header))
        left.append(f'<div class="brand">{brand}</div>')
    if len(tabs) >= 2 or (tabs and cfg["tabs"]["show_single"]):
        left.append(f'<nav class="tabs">{"".join(link(t) for t in tabs)}</nav>')
    about = cfg["page"]["about_tab"]
    if active and active not in tabs and active != about:
        right.append(link(active, " sub"))
    if about and page_path(cfg, about):
        right.append(link(about, " about"))
    if live and cfg["page"]["live_reload"]:
        right.append(f'<span class="live" title="{t(cfg, "live_title")}">●</span>')
    if not left and not right:
        return ""
    return f'<header class="topbar">{"".join(left)}<div class="right">{"".join(right)}</div></header>'


# ------------------------------------------------------ notes and tasks ----
# Note: lines between {{note}} and {{/note}} -> a textarea that saves back into the md file.
# Tasks: plain md tasks (- [ ] …) can be toggled, added and deleted in user tabs.
# The n-th checkbox on the page = the n-th task line in the file.

NOTE_OPEN, NOTE_CLOSE = "{{note}}", "{{/note}}"
TASK_LINE_RE = re.compile(r"^(\s*(?:>\s?)*\s*(?:[-*+]|\d+[.)])\s+)\[([ xX])\](\s.*)?$")
CHECKBOX_RE = re.compile(r'<input type="checkbox" disabled( checked)?/>')


def source_lines(text):
    """(number, line, kind): kind = code | note | marker | normal."""
    fence, in_note = None, False
    for i, line in enumerate(text.split("\n")):
        s = line.strip()
        if in_note:
            if s == NOTE_CLOSE:
                in_note = False
                yield i, line, "marker"
            else:
                yield i, line, "note"
            continue
        m = FENCE_RE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            yield i, line, "code"
            continue
        if m:
            fence = m.group(1)
            yield i, line, "code"
            continue
        if s == NOTE_OPEN:
            in_note = True
            yield i, line, "marker"
            continue
        yield i, line, "normal"


def task_lines(text):
    return [i for i, line, k in source_lines(text) if k == "normal" and TASK_LINE_RE.match(line)]


def tasks_sig(text):
    lines = text.split("\n")
    return hashlib.sha1("\n".join(lines[i] for i in task_lines(text)).encode()).hexdigest()[:16]


def note_ranges(text):
    """[(open_line, close_line)] — the closing line may be missing (end of file)."""
    out, start = [], None
    for i, line, k in source_lines(text):
        if k == "marker":
            if start is None:
                start = i
            else:
                out.append((start, i))
                start = None
    if start is not None:
        out.append((start, len(text.split("\n"))))
    return out


def extract_notes(cfg, text, fname, editable):
    """Replaces notes with placeholder lines (kept out of markdown) and returns {placeholder: html}."""
    lines, out, tokens = text.split("\n"), [], {}
    ranges = note_ranges(text)
    pos = 0
    for n, (a, b) in enumerate(ranges):
        out += lines[pos:a]
        body = "\n".join(lines[a + 1:b])
        tok = f"H6082NOTE{n}X{secrets.token_hex(4)}"
        ro = "" if editable else " readonly"
        attrs = f' data-file="{html.escape(fname)}" data-i="{n}" data-live-hold' if editable else ""
        tokens[tok] = (f'<div class="note-box"><textarea class="note-area"{attrs}{ro} rows="2" spellcheck="false" '
                       f'aria-label="{t(cfg, "note_aria")}">\n{html.escape(body)}</textarea>'
                       f'<small class="note-st"></small></div>')
        out += ["", tok, ""]
        pos = b + 1
    out += lines[pos:]
    return "\n".join(out), tokens


def number_tasks(cfg, body, count, editable):
    """Numbers the task checkboxes; in an editable tab enables them and adds delete buttons."""
    if not editable:
        return body
    found = len(CHECKBOX_RE.findall(body))
    if found != count:
        log.warning("tasks: %d checkboxes on the page, %d lines in the file — editing disabled", found, count)
        return body
    it = iter(range(count))

    def sub(m):
        i = next(it)
        chk = " checked" if m.group(1) else ""
        return (f'<input type="checkbox" class="task" data-i="{i}"{chk} aria-label="{t(cfg, "task_done_aria")}">'
                f'<button type="button" class="task-del" data-i="{i}" title="{t(cfg, "task_delete")}">✕</button>')
    return CHECKBOX_RE.sub(sub, body)


def build_tab(cfg, tabs, name, embed):
    md = make_md(cfg)
    src = page_path(cfg, name)
    fid = file_id(src)
    raw = src.read_text(encoding="utf-8")
    editable = cfg["editor"]["enabled"] and not is_system(cfg, name) and not embed
    text, notes = extract_notes(cfg, raw, fid, editable)
    text = expand_shortcodes(cfg, text)
    cols = "".join(f'<div class="col">{blocks(render_md(md, c))}</div>' for c in split_columns(text))
    for tok, h in notes.items():
        cols = cols.replace(f"<p>{tok}</p>", h)
    cols = number_tasks(cfg, cols, len(task_lines(raw)), editable)
    attrs = f' data-file="{html.escape(fid)}" data-tasks-sig="{tasks_sig(raw)}"' if editable else ""
    bar = "" if embed else tab_bar(cfg, tabs, name)
    body = f'{bar}<div class="grid"{attrs}>{cols}</div>'
    title = cfg["page"]["title"]
    if len(tabs) > 1 or name not in tabs:
        title = f"{tab_label(cfg, name)} · {title}"
    check_s = int(cfg["checks"]["interval_s"]) if cfg["checks"]["enabled"] else 0
    sys_s = int(cfg["system"]["interval_s"]) if cfg["system"]["enabled"] else 0
    scripts = (LIVE_JS if cfg["page"]["live_reload"] else "") + \
        PAGE_JS.replace("__CHECK_S__", str(check_s)).replace("__SYS_S__", str(sys_s))
    return page(cfg, title, postprocess(body, cfg), scripts, "embed" if embed else "")


def build_message(cfg, tabs, msg):
    return page(cfg, cfg["page"]["title"], f'{tab_bar(cfg, tabs, None, live=False)}<div class="grid"><div class="col">'
                f'<section class="block"><div class="block-body"><p>{msg}</p></div></section></div></div>')


def build_editor(cfg, tabs, fname):
    stem = None if fname == "config.toml" else tab_of(fname)
    m = SYSTEM_FILE_RE.match(fname) or LANG_SUFFIX_RE.match(Path(fname).stem)
    plang = m.group(1) if SYSTEM_FILE_RE.match(fname) else (m.group(2) if m else "en")
    preview = stem or default_tab(cfg, tabs)
    about = cfg["page"]["about_tab"] or ""
    view = f'<a class="tab" href="/{quote(stem)}?lang={plang}">{t(cfg, "ed_view")}</a>' if stem else ""
    if cfg["history"]["enabled"]:
        view += f'<a class="tab" href="/history/{quote(fname)}">{t(cfg, "ed_history")}</a>'

    q = f"?embed=1&lang={plang}" if stem else "?embed=1"
    iframe = (f'<iframe src="/{quote(preview)}{q}" title="{t(cfg, "ed_preview")}"></iframe>'
              if preview else "")
    body = f"""{tab_bar(cfg, tabs, None, live=False)}
<div class="editor">
  <div class="ed-head">
    <span class="ed-name">✎ {html.escape(fname)}</span>
    <span id="status" class="st">{t(cfg, "loading")}</span>
    <span id="conflict" hidden><button id="reload">{t(cfg, "ed_reload")}</button><button id="force">{t(cfg, "ed_force")}</button></span>
    <span class="ed-right">{view}<a class="tab" href="/{quote(about)}">{t(cfg, "ed_back")}</a></span>
  </div>
  <div class="ed-panes">
    <textarea id="src" spellcheck="false" autocapitalize="off" autocomplete="off" disabled></textarea>
    {iframe}
  </div>
</div>"""
    js = EDITOR_JS.replace("__SMART__", SMART_JS).replace("__NAME__", json.dumps(fname)).replace("__DELAY__", str(int(cfg["editor"]["autosave_ms"])))
    return page(cfg, f"✎ {fname} · {cfg['page']['title']}", body, js, "editing")


# ----------------------------------------------------------------- cache ----

_cache = {}
_lock = threading.Lock()


def with_lang(cfg, lang):
    """Config copy with a different language (?lang=… preview, nothing is saved)."""
    if lang not in LANGS or lang == cur_lang(cfg):
        return cfg
    return {**cfg, "page": {**cfg["page"], "lang": lang}}


def render_tab(name, embed=False, lang=None):
    """Returns (status, html_bytes). Cached by file mtime, config, file list and language."""
    with _lock:
        cfg = with_lang(load_config(), lang)
        tabs = list_tabs(cfg)
        if name is None:
            name = default_tab(cfg, tabs)
            if name is None:
                return 200, build_message(cfg, tabs, t(cfg, "msg_no_pages")).encode()
        f = page_path(cfg, name) if TAB_RE.match(name) and not LANG_SUFFIX_RE.match(name) else None
        if f is None:
            return 404, build_message(cfg, tabs, t(cfg, "msg_no_tab", name=html.escape(name))).encode()
        key = (str(f), mtime(f), _cfg["mtime"], tuple(all_stems()), cur_lang(cfg))
        hit = _cache.get((name, embed, cur_lang(cfg)))
        if hit and hit[0] == key:
            return 200, hit[1]
        try:
            out = build_tab(cfg, tabs, name, embed).encode("utf-8")
        except Exception:
            log.exception("render %s failed", name)
            if hit:
                return 200, hit[1]
            raise
        _cache[(name, embed, cur_lang(cfg))] = (key, out)
        log.info("rendered: %s%s [%s]", name, " (embed)" if embed else "", cur_lang(cfg))
        return 200, out


# ---------------------------------------------------------------- editor ----

SYSTEM_FILE_RE = re.compile(r"^system/(" + "|".join(LANGS) + r")/([A-Za-z0-9][A-Za-z0-9_.-]*)\.md$")


def editable_path(fname):
    """Only config.toml, pages/<name>.md and system/<lang>/<name>.md — nothing else."""
    if fname == "config.toml":
        return CFG_FILE
    if m := SYSTEM_FILE_RE.match(fname):
        return SYSTEM / m.group(1) / f"{m.group(2)}.md"
    if fname.endswith(".md") and "/" not in fname and TAB_RE.match(fname[:-3]):
        return PAGES / fname
    return None


def tab_of(fname):
    """Tab name for a file id: demo.cs.md -> demo, system/en/h6082.md -> h6082."""
    stem = Path(fname).stem
    m = LANG_SUFFIX_RE.match(stem)
    return m.group(1) if m and "/" not in fname else stem


# --------------------------------------------------------------- history ----
# Snapshots of a file's state BEFORE a change in content/.history/<file>/<version>.snap.
# Changes within [history] coalesce_min minutes of the last snapshot are merged.
# Catches the editor and edits made elsewhere (vim, git) — watched by history_watcher.

HIST = CONTENT / ".history"
HIST_LOCK = threading.Lock()
V_RE = re.compile(r"^\d{8}-\d{6}(?:-\d+)?$")
KEEP_MIN = 3   # newest versions retention never deletes


def tracked_files():
    files = {p.name: p for p in sorted(PAGES.glob("*.md")) if TAB_RE.match(p.stem)}
    files.update({file_id(p): p for p in system_files()})
    files["config.toml"] = CFG_FILE
    return files


def versions(fname):
    """[(version, path, time)] newest first."""
    d = HIST / fname
    if not d.is_dir():
        return []
    out = [(p.stem, p, p.stat().st_mtime) for p in d.glob("*.snap") if V_RE.match(p.stem)]
    return sorted(out, key=lambda x: x[2], reverse=True)


def snapshot(fname, text, cfg, force=False):
    """Stores `text` (state before a change) as a new version; returns True if one was created."""
    H = cfg["history"]
    vers = versions(fname)
    if vers and not force and time.time() - vers[0][2] < float(H["coalesce_min"]) * 60:
        return False
    if vers and vers[0][1].read_text(encoding="utf-8") == text:
        return False
    d = HIST / fname
    d.mkdir(parents=True, exist_ok=True)
    v = time.strftime("%Y%m%d-%H%M%S")
    p, i = d / f"{v}.snap", 1
    while p.exists():
        p, i = d / f"{v}-{i}.snap", i + 1
    write_atomic(p, text)
    now = time.time()
    for idx, (_, vp, ts) in enumerate(versions(fname)):
        if idx >= KEEP_MIN and (idx >= int(H["max_versions"]) or now - ts > float(H["max_age_days"]) * 86400):
            vp.unlink(missing_ok=True)
    return True


def history_watcher():
    """Every 2 s compares files with their last known content; on change stores the previous state."""
    mem = {}
    for n, p in tracked_files().items():
        try:
            mem[n] = (mtime(p), p.read_text(encoding="utf-8"))
        except OSError:
            pass
    while True:
        time.sleep(2)
        try:
            cfg = load_config()
            files = tracked_files()
            for n, p in files.items():
                m = mtime(p)
                old = mem.get(n)
                if m is None or (old and old[0] == m):
                    continue
                text = p.read_text(encoding="utf-8")
                if old and old[1] != text and cfg["history"]["enabled"]:
                    with HIST_LOCK:
                        if snapshot(n, old[1], cfg):
                            log.info("history: new version of %s", n)
                mem[n] = (m, text)
            for n in set(mem) - set(files):
                del mem[n]
        except Exception:  # noqa: BLE001 — the thread must not die
            log.exception("history watcher")


def _after_text(fname, idx, vers):
    """Content after the change that started at version idx: the newer version or the current file."""
    if idx > 0:
        return vers[idx - 1][1].read_text(encoding="utf-8")
    p = tracked_files().get(fname)
    return p.read_text(encoding="utf-8") if p and p.exists() else ""


def diff_stats(a, b):
    add = rem = 0
    for line in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0):
        if line.startswith("+") and not line.startswith("+++"):
            add += 1
        elif line.startswith("-") and not line.startswith("---"):
            rem += 1
    return add, rem


def history_items(fname=None, limit=10):
    files = [fname] if fname else list(tracked_files())
    rows = []
    for f in files:
        rows += [(f, i, v) for i, v in enumerate(versions(f))]
    rows.sort(key=lambda r: r[2][2], reverse=True)
    out = []
    for f, i, (v, p, ts) in rows[:limit]:
        vers = versions(f)
        a, b = p.read_text(encoding="utf-8"), _after_text(f, i, vers)
        add, rem = diff_stats(a, b)
        out.append({"file": f, "v": v, "ts": int(ts), "added": add, "removed": rem})
    return out


def diff_html(a, b, la, lb):
    out = []
    for line in difflib.unified_diff(a.splitlines(), b.splitlines(), la, lb, lineterm="", n=3):
        cls = ("dh" if line.startswith(("---", "+++")) else "hk" if line.startswith("@@")
               else "da" if line.startswith("+") else "dd" if line.startswith("-") else "")
        out.append(f'<span class="{cls}">{html.escape(line) or " "}</span>')
    return f'<pre class="diff">{chr(10).join(out)}</pre>' if out else ""


HISTORY_JS = """<script nonce="__NONCE__">
(() => {
  const T = __T__;
  const H = {'X-H6082': '1', 'Content-Type': 'application/json'};
  const fmt = (ts) => new Date(ts * 1000).toLocaleString(T.locale,
    {day: 'numeric', month: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit'});
  document.querySelectorAll('time[data-ts]').forEach((t) => { t.textContent = fmt(+t.dataset.ts); });
  document.addEventListener('click', async (e) => {
    const b = e.target.closest('button[data-act]');
    if (!b) return;
    const f = b.dataset.file, act = b.dataset.act;
    const msg = act === 'restore'
      ? T.confirm_restore.replace('{f}', f).replace('{w}', b.dataset.when)
      : T.confirm_purge.replace('{f}', f);
    if (!confirm(msg)) return;
    const r = await fetch('/api/history/' + act, {method: 'POST', headers: H,
      body: JSON.stringify({file: f, v: b.dataset.v || ''})});
    const j = await r.json().catch(() => ({}));
    if (!r.ok) { alert(j.error || r.status); return; }
    location.href = act === 'restore' ? '/edit/' + encodeURIComponent(f) : location.pathname;
  });
})();
</script>"""


def build_history(cfg, tabs, fname, v):
    vers = versions(fname)
    rows = []
    for i, (ver, p, ts) in enumerate(vers):
        add, rem = diff_stats(p.read_text(encoding="utf-8"), _after_text(fname, i, vers))
        cur = " class=\"cur\"" if ver == v else ""
        rows.append(f'<li{cur}><a href="?v={quote(ver)}"><time data-ts="{int(ts)}"></time></a>'
                    f'<span class="h-add"> +{add}</span><span class="h-del"> −{rem}</span></li>')
    lst = (f'<ul class="hist-list">{"".join(rows)}</ul>' if rows
           else f"<p><small>{t(cfg, 'h_no_versions')}</small></p>")
    purge = (f'<p><button data-act="purge" data-file="{html.escape(fname)}">{t(cfg, "h_purge")}</button></p>'
             if rows else "")
    explain = t(cfg, "h_explain", min=int(cfg["history"]["coalesce_min"]))
    left = (f'<section class="block"><h2>{t(cfg, "h_versions")} · {html.escape(fname)}</h2>'
            f'<div class="block-body">{lst}<p><small>{explain}</small></p>{purge}</div></section>')
    idx = next((i for i, x in enumerate(vers) if x[0] == v), None)
    if idx is None:
        right = (f'<section class="block"><h2>{t(cfg, "h_diff")}</h2><div class="block-body">'
                 f'<p><small>{t(cfg, "h_pick")}</small></p></div></section>')
    else:
        ver, p, ts = vers[idx]
        a = p.read_text(encoding="utf-8")
        b = _after_text(fname, idx, vers)
        lb = t(cfg, "h_current") if idx == 0 else t(cfg, "h_version", v=vers[idx - 1][0])
        diff = diff_html(a, b, t(cfg, "h_version", v=ver), lb) or f"<p><small>{t(cfg, 'h_no_change')}</small></p>"
        right = (f'<section class="block"><h2>{t(cfg, "h_diff")} · <time data-ts="{int(ts)}"></time></h2>'
                 f'<div class="block-body">{diff}'
                 f'<p><button data-act="restore" data-file="{html.escape(fname)}" data-v="{html.escape(ver)}" '
                 f'data-when="{html.escape(ver)}">{t(cfg, "h_restore")}</button> '
                 f'<small>{t(cfg, "h_restore_hint")}</small></p></div></section>')
    nav = f'<p class="hist-nav"><a class="tab" href="/edit/{quote(fname)}">{t(cfg, "h_editor")}</a></p>'
    body = f'{tab_bar(cfg, tabs, None, live=False)}{nav}<div class="grid hist">{"".join([left, right])}</div>'
    return page(cfg, f"{t(cfg, 'h_title', name=fname)} · {cfg['page']['title']}", body, HISTORY_JS, "history")


def write_atomic(path, text):
    """Write to a temp file in the same directory + rename: a file is never half-written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".", suffix=".part")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.chmod(tmp, (path.stat().st_mode & 0o777) if path.exists() else 0o644)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def set_toml_value(text, section, key, literal):
    """Sets `key = literal` in [section], keeping the rest of the file and its comments."""
    lines = text.split("\n")
    sec, start = None, None
    key_re = re.compile(rf"^(\s*{re.escape(key)}\s*=\s*)(\"[^\"]*\"|'[^']*'|[^\s#]+)(.*)$")
    for i, line in enumerate(lines):
        h = re.match(r"^\s*\[([^\[\]]+)\]\s*(?:#.*)?$", line)
        if h:
            if sec == section:
                break
            sec = h.group(1).strip()
            if sec == section:
                start = i
            continue
        if sec == section and (m := key_re.match(line)):
            lines[i] = m.group(1) + literal + m.group(3)
            return "\n".join(lines)
    if start is None:
        return text.rstrip("\n") + f"\n\n[{section}]\n{key} = {literal}\n"
    lines.insert(start + 1, f"{key} = {literal}")
    return "\n".join(lines)


def toml_warning(cfg, text):
    try:
        tomllib.loads(text)
        return None
    except tomllib.TOMLDecodeError as e:
        return t(cfg, "toml_err", e=e)


# --------------------------------------------------------- checks + rss ----

_check_cache, _rss_cache, _net_lock = {}, {}, threading.Lock()
_pool = ThreadPoolExecutor(max_workers=8)


def _short_err(e):
    e = getattr(e, "reason", e)
    return (type(e).__name__ + (f": {e}" if str(e) else ""))[:120]


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects only to http(s) and at most 3 times (no ftp:// etc.)."""
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).scheme not in ("http", "https"):
            raise urllib.error.URLError("redirect outside http(s)")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _open(req, timeout, ctx=None):
    opener = urllib.request.build_opener(_SafeRedirect, urllib.request.HTTPSHandler(context=ctx))
    return opener.open(req, timeout=timeout)


def check_one(target, cfg):
    """HTTP(S): response < 400 = up, 4xx = warn (running, but…), 5xx/error = down. TCP: connect = up."""
    C = cfg["checks"]
    timeout = float(C["timeout_s"])
    t0 = time.monotonic()
    u = urlsplit(target)
    try:
        if u.scheme == "tcp":
            with socket.create_connection((u.hostname, u.port), timeout=timeout):
                pass
            return {"state": "up", "ms": round((time.monotonic() - t0) * 1000)}
        ctx = ssl.create_default_context()
        if not C["verify_tls"]:
            ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
        req = urllib.request.Request(target, headers={"User-Agent": "h6082-check/1"})
        try:
            with _open(req, timeout, ctx) as r:
                code = r.status
        except urllib.error.HTTPError as e:
            code = e.code
        state = "up" if code < 400 else "warn" if code < 500 else "down"
        return {"state": state, "status": code, "ms": round((time.monotonic() - t0) * 1000)}
    except Exception as e:  # noqa: BLE001 — any error = unreachable
        return {"state": "down", "error": _short_err(e)}


def run_checks(targets, cfg):
    ttl = max(5, int(cfg["checks"]["interval_s"]) - 5)
    now = time.time()
    with _net_lock:
        todo = [t for t in targets if not (_check_cache.get(t) and now - _check_cache[t][0] < ttl)]
    for t, res in zip(todo, _pool.map(lambda t: check_one(t, cfg), todo)):
        with _net_lock:
            _check_cache[t] = (time.time(), res)
    with _net_lock:
        return {t: _check_cache[t][1] for t in targets if t in _check_cache}


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _parse_date(s):
    if not s:
        return None
    try:
        return int(email.utils.parsedate_to_datetime(s).timestamp())
    except (TypeError, ValueError, IndexError):
        pass
    try:
        return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())
    except ValueError:
        return None


def parse_feed(data):
    """RSS 2.0 / RSS 1.0 (RDF) / Atom -> [{title, link, comments, ts}]. Parsuje defusedxml."""
    root = SafeET.fromstring(data)
    items = []
    for el in root.iter():
        if _local(el.tag) not in ("item", "entry"):
            continue
        it = {"title": "", "link": "", "comments": "", "ts": None}
        for c in el:
            n, text = _local(c.tag), (c.text or "").strip()
            if n == "title":
                it["title"] = text
            elif n == "link":
                href = c.get("href")
                if href and c.get("rel", "alternate") == "alternate":
                    it["link"] = href
                elif not href and text:
                    it["link"] = text
            elif n == "comments":
                it["comments"] = text
            elif n in ("pubDate", "published", "updated", "date") and it["ts"] is None:
                it["ts"] = _parse_date(text)
        it["link"] = it["link"] if valid_http(it["link"]) else ""
        it["comments"] = it["comments"] if valid_http(it["comments"]) else ""
        if it["title"] and it["link"]:
            items.append(it)
    return items


def get_feed(url, cfg):
    R = cfg["rss"]
    with _net_lock:
        hit = _rss_cache.get(url)
    if hit and time.time() - hit[0] < float(R["refresh_min"]) * 60:
        return hit[1]
    req = urllib.request.Request(url, headers={"User-Agent": "h6082-rss/1",
                                               "Accept": "application/rss+xml, application/atom+xml, */*"})
    try:
        with _open(req, float(R["timeout_s"]), ssl.create_default_context()) as r:
            data = r.read(2 * 1024 * 1024 + 1)
        if len(data) > 2 * 1024 * 1024:
            raise ValueError("feed is larger than 2 MB")
        items = parse_feed(data)
    except Exception as e:  # noqa: BLE001
        if hit:  # on failure return the last known state
            log.warning("RSS %s: %s — returning older data", url, _short_err(e))
            return hit[1]
        raise
    with _net_lock:
        _rss_cache[url] = (time.time(), items)
    log.info("RSS %s: %d items", url, len(items))
    return items


# ---------------------------------------------------------------- system ----
# Only safe sources: the host's /proc and /sys are visible in the container (stat, meminfo,
# loadavg, uptime, thermal); disks via statvfs on empty directories mounted from the host.

_sys = {"cpu_prev": None, "cpu_pct": None, "t": 0.0, "data": None}


def _read(path, default=""):
    try:
        return Path(path).read_text().strip()
    except OSError:
        return default


def _cpu_sample():
    f = _read("/proc/stat").split("\n")[0].split()[1:9]
    v = [int(x) for x in f]
    return sum(v), v[3] + v[4]          # total, idle+iowait


def _cpu_pct():
    cur = _cpu_sample()
    prev = _sys["cpu_prev"]
    if prev is None:
        time.sleep(0.25)
        prev, cur = cur, _cpu_sample()
    _sys["cpu_prev"] = cur
    dt, di = cur[0] - prev[0], cur[1] - prev[1]
    if dt > 0:
        _sys["cpu_pct"] = round(100 * (1 - di / dt), 1)
    return _sys["cpu_pct"]


def _meminfo():
    m = {}
    for line in _read("/proc/meminfo").split("\n"):
        k, _, v = line.partition(":")
        if v.strip().endswith("kB"):
            m[k] = int(v.split()[0]) * 1024
    return m


def _temps(cfg):
    zones = []
    for z in sorted(Path("/sys/class/thermal").glob("thermal_zone*")):
        t, typ = _read(z / "temp"), _read(z / "type")
        if t.lstrip("-").isdigit() and int(t) > 0:
            zones.append((typ, round(int(t) / 1000, 1)))
    want = cfg["system"]["temps"]
    if want:
        return [{"label": t, "c": c} for t, c in zones if t in want]
    pkg = [c for t, c in zones if t == "x86_pkg_temp"]
    if pkg:
        return [{"label": "CPU", "c": pkg[0]}]
    return [{"label": "max", "c": max(c for _, c in zones)}] if zones else []


def _disks(cfg):
    out = []
    for d in cfg["system"]["disks"]:
        try:
            st = os.statvfs(d["path"])
        except (OSError, KeyError, TypeError):
            continue
        total = st.f_blocks * st.f_frsize
        free_all, avail = st.f_bfree * st.f_frsize, st.f_bavail * st.f_frsize
        used = total - free_all
        out.append({"label": str(d.get("label", d["path"])), "total": total, "used": used,
                    "pct": round(100 * used / (used + avail), 1) if used + avail else 0})
    return out


def system_info(cfg):
    """System snapshot; cached for 1 s (more open pages do not add load)."""
    with _net_lock:
        if _sys["data"] and time.monotonic() - _sys["t"] < 1:
            return _sys["data"]
    m = _meminfo()
    la = _read("/proc/loadavg", "0 0 0").split()[:3]
    data = {
        "cpu": {"pct": _cpu_pct()},
        "mem": {"total": m.get("MemTotal", 0), "used": m.get("MemTotal", 0) - m.get("MemAvailable", 0)},
        "swap": {"total": m.get("SwapTotal", 0), "used": m.get("SwapTotal", 0) - m.get("SwapFree", 0)},
        "load": [float(x) for x in la],
        "uptime": int(float(_read("/proc/uptime", "0").split()[0])),
        "temp": _temps(cfg),
        "disk": _disks(cfg),
    }
    with _net_lock:
        _sys["data"], _sys["t"] = data, time.monotonic()
    return data


# ------------------------------------------------------------------ http ----

MIME = {".css": "text/css; charset=utf-8", ".woff2": "font/woff2", ".svg": "image/svg+xml",
        ".png": "image/png", ".ico": "image/x-icon", ".js": "text/javascript", ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".avif": "image/avif"}


class Handler(BaseHTTPRequestHandler):
    server_version = "h6082"
    sys_version = ""
    timeout = 30  # socket timeout: a slow / stuck client does not hold a thread forever

    # ---- protections shared by all requests
    def _host_ok(self):
        """Against DNS rebinding: answer only to a Host from [api] allowed_hosts (healthcheck always)."""
        if urlsplit(self.path).path == "/healthz":
            return True
        allowed = allowed_hosts(load_config())
        host = urlsplit("//" + (self.headers.get("Host") or "")).hostname or ""
        if host.lower() in allowed:
            return True
        self._send(421, (t(load_config(), "err_host_421", host=host) + "\n").encode(), "text/plain; charset=utf-8")
        return False

    def _auth_ok(self):
        """HTTP Basic for the editor and writes, if H6082_EDITOR_PASSWORD is set in the environment."""
        if not EDITOR_PASSWORD:
            return True
        h = self.headers.get("Authorization") or ""
        if h.startswith("Basic "):
            try:
                user, _, pw = base64.b64decode(h[6:]).decode("utf-8").partition(":")
            except (ValueError, UnicodeDecodeError):
                user, pw = "", ""
            if hmac.compare_digest(user.encode(), EDITOR_USER.encode()) & \
                    hmac.compare_digest(pw.encode(), EDITOR_PASSWORD.encode()):
                return True
            time.sleep(1)  # slows down password guessing
            log.warning("failed editor login from %s", self.address_string())
        body = b"401 - editor vyzaduje prihlaseni\n"
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="h6082 editor", charset="UTF-8"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        return False

    def _cookie(self, name):
        """A visitor preference cookie — used only in read-only mode (nothing is stored server-side)."""
        if not READONLY:
            return ""
        m = re.search(rf"(?:^|;\s*){name}=([^;]*)", self.headers.get("Cookie") or "")
        return unquote(m.group(1)) if m else ""

    def _theme(self):
        """Theme = [theme] default from the config; ?theme=… is a preview for one request only."""
        cfg = load_config()
        q = parse_qs(urlsplit(self.path).query).get("theme", [""])[0] or self._cookie("h6082_theme")
        names = theme_names(cfg)
        if q in names:
            return q
        d = cfg["theme"]["default"]
        return d if d in names else "obsidian"

    def _send(self, code, body, ctype, cache="no-cache"):
        csp = None
        if ctype.startswith("text/html"):
            body = body.replace(b'data-theme="__THEME__"', f'data-theme="{self._theme()}"'.encode(), 1)
            nonce = secrets.token_urlsafe(16)
            body = body.replace(NONCE_PH.encode(), nonce.encode())
            csp = (f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; style-src 'self' 'unsafe-inline'; "
                   "img-src 'self' data: https: http:; connect-src 'self'; frame-src 'self'; "
                   "frame-ancestors 'self'; base-uri 'none'; form-action 'self'; object-src 'none'")
        elif ctype.startswith("image/"):
            # an image opened directly (mainly SVG) must not run scripts or load anything
            csp = "default-src 'none'; style-src 'unsafe-inline'; img-src data:; sandbox"
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        if csp:
            self.send_header("Content-Security-Policy", csp)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def _api_denied(self, cfg, editor=True):
        """API guard: editor enabled, allowed Host/Origin (against DNS rebinding and foreign sites)
        and the custom X-H6082 header (a cross-origin request with it needs a CORS preflight,
        which the server never allows, so the browser blocks it)."""
        if editor and not cfg["editor"]["enabled"]:
            return t(cfg, "err_editor_off")
        allowed = allowed_hosts(cfg)
        host = urlsplit("//" + (self.headers.get("Host") or "")).hostname or ""
        if host.lower() not in allowed:
            return t(cfg, "err_host", host=host)
        origin = self.headers.get("Origin")
        if origin and (urlsplit(origin).hostname or "").lower() not in allowed:
            return t(cfg, "err_origin")
        if self.headers.get("X-H6082") != "1":
            return t(cfg, "err_header")
        return None

    def _read_json(self, cfg):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise ValueError(t(cfg, "err_cl")) from None
        if n < 0:
            raise ValueError(t(cfg, "err_cl"))
        if n > int(cfg["editor"]["max_size_kb"]) * 1024:
            raise ValueError(t(cfg, "err_too_big"))
        data = json.loads(self.rfile.read(n) or b"{}")
        if not isinstance(data, dict):
            raise ValueError(t(cfg, "err_json"))
        return data

    # ---- GET
    def do_GET(self):
        if not self._host_ok():
            return
        u = urlsplit(self.path)
        path, qs = unquote(u.path), parse_qs(u.query)
        if path == "/healthz":
            return self._send(200, b"ok\n", "text/plain")
        if path == "/events":
            if READONLY:  # nothing ever changes, no long-lived connections for the public
                return self._send(404, b"404\n", "text/plain")
            return self._events()
        if path == "/themes.css":
            return self._themes_css()
        if path.startswith("/media/"):
            name = path[len("/media/"):]
            f = MEDIA / name if (MEDIA / name).is_file() else DEFAULTS_DIR / "media" / name
            if MEDIA_RE.match(name) and f.is_file() and f.resolve().parent in (MEDIA.resolve(),
                                                                              (DEFAULTS_DIR / "media").resolve()):
                # no-cache: own images change and the change should show at once
                return self._send(200, f.read_bytes(), MIME.get(f.suffix.lower(), "application/octet-stream"))
            return self._send(404, b"404\n", "text/plain")
        if path.startswith("/static/"):
            f = (STATIC / path[len("/static/"):]).resolve()
            if f.is_file() and STATIC in f.parents:
                return self._send(200, f.read_bytes(), MIME.get(f.suffix, "application/octet-stream"),
                                  "public, max-age=3600")
            return self._send(404, b"404\n", "text/plain")
        if path == "/api/file":
            return self._api_get(qs.get("name", [""])[0])
        if path == "/api/sys":
            cfg = load_config()
            if err := self._api_denied(cfg, editor=False):
                return self._json(403, {"error": err})
            if not cfg["system"]["enabled"]:
                return self._json(403, {"error": t(cfg, "err_sys_off")})
            return self._json(200, system_info(cfg))
        if path == "/api/rss":
            return self._api_rss(qs)
        if path == "/api/history":
            return self._api_history(qs)
        if path.startswith("/history/"):
            return self._history_page(path[len("/history/"):], qs.get("v", [""])[0])
        if path.startswith("/edit/"):
            return self._editor(path[len("/edit/"):])
        name = path.strip("/") or None
        if name and name.endswith(".md"):
            name = name[:-3]
        lang = qs.get("lang", [None])[0] or self._cookie("h6082_lang") or None
        code, body = render_tab(name, embed=qs.get("embed") == ["1"], lang=lang)
        self._send(code, body, "text/html; charset=utf-8")

    def _themes_css(self):
        with _lock:
            cfg = load_config()
            key = ("themes.css", _cfg["mtime"])
            hit = _cache.get("themes.css")
            if not hit or hit[0] != key:
                hit = (key, themes_css(cfg).encode())
                _cache["themes.css"] = hit
        self._send(200, hit[1], "text/css; charset=utf-8", "public, max-age=86400")

    def do_HEAD(self):
        self.do_GET()

    def _editor(self, fname):
        if not self._auth_ok():
            return
        with _lock:
            cfg = load_config()
            tabs = list_tabs(cfg)
            p = editable_path(fname)
            if not cfg["editor"]["enabled"]:
                code, body = 403, build_message(cfg, tabs, t(cfg, "msg_editor_disabled"))
            elif p is None or not (p.is_file() or default_of(p)):
                code, body = 404, build_message(cfg, tabs, t(cfg, "msg_not_editable", name=html.escape(fname)))
            else:
                code, body = 200, build_editor(cfg, tabs, fname)
        self._send(code, body.encode(), "text/html; charset=utf-8")

    def _api_get(self, fname):
        cfg = load_config()
        if err := self._api_denied(cfg):
            return self._json(403, {"error": err})
        if not self._auth_ok():
            return
        p = editable_path(fname)
        src = p if p is not None and p.is_file() else (default_of(p) if p is not None else None)
        if src is None:
            return self._json(404, {"error": t(cfg, "err_file_missing")})
        text = src.read_text(encoding="utf-8")
        warn = toml_warning(cfg, text) if p == CFG_FILE else None
        self._json(200, {"name": fname, "text": text, "mtime": str(mtime(p)), "warning": warn})

    def _api_rss(self, qs):
        cfg = load_config()
        if err := self._api_denied(cfg, editor=False):
            return self._json(403, {"error": err})
        if not cfg["rss"]["enabled"]:
            return self._json(403, {"error": t(cfg, "err_rss_off")})
        url = qs.get("url", [""])[0]
        if url not in FEEDS:
            return self._json(403, {"error": t(cfg, "err_feed_not_allowed")})
        limit = qs.get("limit", ["10"])[0]
        limit = max(1, min(100, int(limit))) if limit.isdigit() else 10
        try:
            items = get_feed(url, cfg)
        except Exception as e:  # noqa: BLE001
            log.warning("RSS %s selhalo: %s", url, _short_err(e))
            return self._json(502, {"error": t(cfg, "err_feed_load", e=_short_err(e))})
        self._json(200, {"items": items[:limit]})

    # ---- writes from page widgets (theme, language, notes, tasks) — always with the editor password
    def _write_guard(self):
        """Shared checks; returns (cfg, data) or None if an error response was already sent."""
        cfg = load_config()
        if err := self._api_denied(cfg):
            self._json(403, {"error": err})
            return None
        if not self._auth_ok():
            return None
        try:
            return cfg, self._read_json(cfg)
        except ValueError as e:
            self._json(400, {"error": str(e)})
            return None

    def _user_md(self, cfg, fname):
        p = editable_path(fname)
        if p is None or p == CFG_FILE or not p.is_file():
            self._json(404, {"error": t(cfg, "err_file_missing")})
            return None
        if is_system(cfg, p.stem):
            self._json(403, {"error": t(cfg, "err_widget_system")})
            return None
        return p

    def _api_theme(self):
        if not (g := self._write_guard()):
            return
        cfg, data = g
        t = str(data.get("theme", ""))
        if t not in theme_names(cfg):
            return self._json(400, {"error": t(cfg, "err_unknown_theme")})
        with _lock:
            text = CFG_FILE.read_text(encoding="utf-8")
            new = set_toml_value(text, "theme", "default", json.dumps(t))
            try:
                if tomllib.loads(new).get("theme", {}).get("default") != t:
                    raise ValueError
            except (tomllib.TOMLDecodeError, ValueError):
                return self._json(500, {"error": t(cfg, "err_config_edit")})
            if new != text:
                write_atomic(CFG_FILE, new)
        log.info("theme set to %s", t)
        self._json(200, {"ok": True})

    def _api_lang(self):
        if not (g := self._write_guard()):
            return
        cfg, data = g
        lang = str(data.get("lang", ""))
        if lang not in LANGS:
            return self._json(400, {"error": t(cfg, "err_unknown_lang")})
        with _lock:
            text = CFG_FILE.read_text(encoding="utf-8")
            new = set_toml_value(text, "page", "lang", json.dumps(lang))
            try:
                if tomllib.loads(new).get("page", {}).get("lang") != lang:
                    raise ValueError
            except (tomllib.TOMLDecodeError, ValueError):
                return self._json(500, {"error": t(cfg, "err_config_edit")})
            if new != text:
                write_atomic(CFG_FILE, new)
        log.info("language set to %s", lang)
        self._json(200, {"ok": True})

    def _api_note(self):
        if not (g := self._write_guard()):
            return
        cfg, data = g
        if not (p := self._user_md(cfg, str(data.get("file", "")))):
            return
        i, orig, new = data.get("i"), data.get("orig"), data.get("text")
        if not isinstance(i, int) or not isinstance(orig, str) or not isinstance(new, str):
            return self._json(400, {"error": t(cfg, "err_bad_request")})
        new = new.replace("\r\n", "\n").replace("\r", "\n")
        if any(x.strip() in (NOTE_OPEN, NOTE_CLOSE) for x in new.split("\n")):
            return self._json(400, {"error": t(cfg, "err_note_markers")})
        with _lock:
            text = p.read_text(encoding="utf-8")
            ranges = note_ranges(text)
            if not 0 <= i < len(ranges):
                return self._json(409, {"error": t(cfg, "err_note_changed")})
            a, b = ranges[i]
            lines = text.split("\n")
            if "\n".join(lines[a + 1:b]) != orig:
                return self._json(409, {"error": t(cfg, "err_note_changed")})
            closing = lines[b:b + 1] or [NOTE_CLOSE]
            lines[a + 1:b + 1] = (new.split("\n") if new else []) + closing
            write_atomic(p, "\n".join(lines))
        self._json(200, {"ok": True})

    def _api_tasks(self):
        if not (g := self._write_guard()):
            return
        cfg, data = g
        if not (p := self._user_md(cfg, str(data.get("file", "")))):
            return
        op = data.get("op")
        with _lock:
            text = p.read_text(encoding="utf-8")
            if data.get("sig") != tasks_sig(text):
                return self._json(409, {"error": t(cfg, "err_tasks_changed")})
            lines, idx = text.split("\n"), task_lines(text)
            try:
                if op == "toggle":
                    ln = idx[int(data["i"])]
                    m = TASK_LINE_RE.match(lines[ln])
                    mark = " " if m.group(2) in "xX" else "x"
                    lines[ln] = f"{m.group(1)}[{mark}]{m.group(3) or ''}"
                elif op == "delete":
                    ln = idx[int(data["i"])]
                    ind = len(lines[ln]) - len(lines[ln].lstrip())
                    end = ln + 1
                    while end < len(lines) and lines[end].strip() and \
                            len(lines[end]) - len(lines[end].lstrip()) > ind:
                        end += 1  # including nested subtasks
                    del lines[ln:end]
                elif op == "add":
                    label = " ".join(str(data.get("text", "")).split())[:300]
                    label = label.replace("<", "&lt;").replace(">", "&gt;")  # text, ne HTML
                    if not label:
                        return self._json(400, {"error": t(cfg, "err_empty_task")})
                    first, last = idx[int(data["first"])], idx[int(data["last"])]
                    prefix = TASK_LINE_RE.match(lines[first]).group(1)
                    prefix = re.sub(r"\d+([.)])", r"1\1", prefix)
                    ind = len(lines[last]) - len(lines[last].lstrip())
                    end = last + 1
                    while end < len(lines) and lines[end].strip() and \
                            len(lines[end]) - len(lines[end].lstrip()) > ind:
                        end += 1
                    lines.insert(end, f"{prefix}[ ] {label}")
                else:
                    return self._json(400, {"error": t(cfg, "err_unknown_op")})
            except (KeyError, IndexError, ValueError, TypeError, AttributeError):
                return self._json(400, {"error": t(cfg, "err_bad_task")})
            new = "\n".join(lines)
            write_atomic(p, new)
        self._json(200, {"ok": True, "sig": tasks_sig(new)})

    # ---- history
    def _api_history(self, qs):
        cfg = load_config()
        if err := self._api_denied(cfg, editor=False):
            return self._json(403, {"error": err})
        if not cfg["history"]["enabled"]:
            return self._json(403, {"error": t(cfg, "err_history_off")})
        f = qs.get("file", [""])[0] or None
        if f and not editable_path(f):
            return self._json(400, {"error": t(cfg, "err_bad_file")})
        lim = qs.get("limit", ["10"])[0]
        lim = max(1, min(100, int(lim))) if lim.isdigit() else 10
        with HIST_LOCK:
            self._json(200, {"items": history_items(f, lim)})

    def _history_page(self, fname, v):
        if not self._auth_ok():
            return
        cfg = load_config()
        tabs = list_tabs(cfg)
        if not cfg["history"]["enabled"] or not cfg["editor"]["enabled"]:
            body = build_message(cfg, tabs, t(cfg, "msg_history_disabled"))
            return self._send(403, body.encode(), "text/html; charset=utf-8")
        if not editable_path(fname):
            body = build_message(cfg, tabs, t(cfg, "msg_no_history", name=html.escape(fname)))
            return self._send(404, body.encode(), "text/html; charset=utf-8")
        with HIST_LOCK:
            body = build_history(cfg, tabs, fname, v if V_RE.match(v or "") else "")
        self._send(200, body.encode(), "text/html; charset=utf-8")

    def _api_history_write(self, act):
        cfg = load_config()
        if err := self._api_denied(cfg):
            return self._json(403, {"error": err})
        if not self._auth_ok():
            return
        if not cfg["history"]["enabled"]:
            return self._json(403, {"error": t(cfg, "err_history_off")})
        try:
            data = self._read_json(cfg)
        except ValueError as e:
            return self._json(400, {"error": str(e)})
        fname, v = str(data.get("file", "")), str(data.get("v", ""))
        p = editable_path(fname)
        if p is None:
            return self._json(400, {"error": t(cfg, "err_bad_file")})
        with HIST_LOCK:
            if act == "purge":
                d = HIST / fname
                for x in d.glob("*.snap"):
                    x.unlink(missing_ok=True)
                if d.is_dir():
                    d.rmdir()
                log.info("history of %s deleted", fname)
                return self._json(200, {"ok": True})
            ver = next((x for x in versions(fname) if x[0] == v), None) if V_RE.match(v) else None
            if ver is None:
                return self._json(404, {"error": t(cfg, "err_version_missing")})
            old = ver[1].read_text(encoding="utf-8")
            try:
                if p.exists():
                    snapshot(fname, p.read_text(encoding="utf-8"), cfg, force=True)
                with _lock:
                    write_atomic(p, old)
            except OSError as e:
                return self._json(500, {"error": t(cfg, "err_restore_failed", e=e.strerror)})
        log.info("history: %s restored to version %s", fname, v)
        self._json(200, {"ok": True})

    # ---- DELETE /api/file?name=…  (move to content/.trash/)
    def do_DELETE(self):
        if not self._host_ok():
            return
        u = urlsplit(self.path)
        if unquote(u.path) != "/api/file":
            return self._json(404, {"error": t(load_config(), "err_unknown_endpoint")})
        cfg = load_config()
        if err := self._api_denied(cfg):
            return self._json(403, {"error": err})
        if not self._auth_ok():
            return
        fname = parse_qs(u.query).get("name", [""])[0]
        p = editable_path(fname)
        if p is None or p == CFG_FILE or not p.is_file():
            return self._json(404, {"error": t(cfg, "err_file_missing")})
        if fname.startswith("system/") and default_of(p):
            with _lock:
                try:
                    TRASH.mkdir(exist_ok=True)
                    dest = TRASH / f"{p.parent.name}-{p.stem}.{time.strftime('%Y%m%d-%H%M%S')}.md"
                    os.replace(p, dest)
                except OSError as e:
                    return self._json(500, {"error": t(cfg, "err_delete_failed", e=e.strerror)})
            log.info("reset %s to default (override -> %s)", fname, dest.relative_to(CONTENT))
            return self._json(200, {"trash": [str(dest.relative_to(CONTENT))]})
        if fname.startswith("system/") or is_system(cfg, tab_of(fname)):
            return self._json(403, {"error": t(cfg, "err_system_delete", name=fname)})
        # base file -> the whole tab incl. translations; a translation -> only that file
        targets = page_variants(p.stem) if not LANG_SUFFIX_RE.match(p.stem) else [p]
        moved = []
        with _lock:
            try:
                TRASH.mkdir(exist_ok=True)
                stamp = time.strftime("%Y%m%d-%H%M%S")
                for f in targets:
                    dest = TRASH / f"{f.stem}.{stamp}.md"
                    os.replace(f, dest)
                    moved.append(str(dest.relative_to(CONTENT)))
            except OSError as e:
                return self._json(500, {"error": t(cfg, "err_delete_failed", e=e.strerror)})
        log.info("deleted %s -> %s", fname, ", ".join(moved))
        self._json(200, {"trash": moved})

    # ---- PUT /api/file?name=…  (save)
    def do_PUT(self):
        if not self._host_ok():
            return
        u = urlsplit(self.path)
        if unquote(u.path) != "/api/file":
            return self._json(404, {"error": t(load_config(), "err_unknown_endpoint")})
        cfg = load_config()
        if err := self._api_denied(cfg):
            return self._json(403, {"error": err})
        if not self._auth_ok():
            return
        fname = parse_qs(u.query).get("name", [""])[0]
        p = editable_path(fname)
        if p is None or not (p.is_file() or default_of(p)):
            return self._json(404, {"error": t(cfg, "err_file_missing")})
        try:
            data = self._read_json(cfg)
            text = data["text"]
            if not isinstance(text, str):
                raise ValueError(t(cfg, "err_text_string"))
        except (ValueError, KeyError) as e:
            return self._json(400, {"error": str(e)})
        with _lock:
            cur = str(mtime(p))
            if data.get("mtime") is not None and data["mtime"] != cur:
                return self._json(409, {"error": t(cfg, "err_file_changed"), "mtime": cur})
            try:
                write_atomic(p, text)
            except OSError as e:
                log.warning("writing %s failed: %s", p, e)
                return self._json(500, {"error": t(cfg, "err_write_failed", e=e.strerror)})
            new = str(mtime(p))
        log.info("editor saved %s (%d B)", fname, len(text.encode()))
        self._json(200, {"mtime": new, "warning": toml_warning(cfg, text) if p == CFG_FILE else None})

    # ---- POST /api/check  (service status)
    def _api_check(self):
        cfg = load_config()
        if err := self._api_denied(cfg, editor=False):
            return self._json(403, {"error": err})
        if not cfg["checks"]["enabled"]:
            return self._json(403, {"error": t(cfg, "err_checks_off")})
        try:
            targets = self._read_json(cfg).get("targets", [])
        except ValueError as e:
            return self._json(400, {"error": str(e)})
        targets = [t for t in targets if isinstance(t, str) and t in CHECK_TARGETS][:100]
        self._json(200, run_checks(targets, cfg))

    # ---- POST /api/new  (new file)
    def do_POST(self):
        if not self._host_ok():
            return
        path = unquote(urlsplit(self.path).path)
        if path == "/api/check":
            return self._api_check()
        if path == "/api/theme":
            return self._api_theme()
        if path == "/api/lang":
            return self._api_lang()
        if path == "/api/note":
            return self._api_note()
        if path == "/api/tasks":
            return self._api_tasks()
        if path in ("/api/history/restore", "/api/history/purge"):
            return self._api_history_write(path.rsplit("/", 1)[1])
        if path != "/api/new":
            return self._json(404, {"error": t(load_config(), "err_unknown_endpoint")})
        cfg = load_config()
        if err := self._api_denied(cfg):
            return self._json(403, {"error": err})
        if not self._auth_ok():
            return
        try:
            name = str(self._read_json(cfg).get("name", "")).strip()
        except ValueError as e:
            return self._json(400, {"error": str(e)})
        if name.endswith(".md"):
            name = name[:-3]
        base = LANG_SUFFIX_RE.match(name).group(1) if LANG_SUFFIX_RE.match(name) else name
        if not TAB_RE.match(name) or base in RESERVED or is_system(cfg, base):
            return self._json(400, {"error": t(cfg, "err_bad_name")})
        p = PAGES / f"{name}.md"
        with _lock:
            if p.exists():
                return self._json(409, {"error": t(cfg, "err_exists", name=name)})
            try:
                # a translation (name.cs) gets the template in its own language
                m = LANG_SUFFIX_RE.match(name)
                write_atomic(p, t(with_lang(cfg, m.group(2)) if m else cfg, "new_file"))
            except OSError as e:
                return self._json(500, {"error": t(cfg, "err_write_failed", e=e.strerror)})
        log.info("editor created %s.md", name)
        self._json(201, {"name": f"{name}.md"})

    # ---- SSE
    def _events(self):
        """Server-Sent Events: sends `change` when anything in content/ changes."""
        if not SSE_SLOTS.acquire(blocking=False):
            return self._send(503, b"too many /events connections\n", "text/plain")
        try:
            self._events_loop()
        finally:
            SSE_SLOTS.release()

    def _events_loop(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        last, idle = content_signature(), 0
        try:
            self.wfile.write(b"retry: 1000\n\n")
            self.wfile.flush()
            while True:
                time.sleep(0.4)
                cur = content_signature()
                if cur != last:
                    last, idle = cur, 0
                    self.wfile.write(b"data: change\n\n")
                elif (idle := idle + 1) >= 40:
                    idle = 0
                    self.wfile.write(b": ping\n\n")
                else:
                    continue
                self.wfile.flush()
        except OSError:
            return

    def log_message(self, fmt, *args):
        if "/healthz" not in self.path and "/events" not in self.path:
            log.info("%s %s", self.address_string(), fmt % args)


if __name__ == "__main__":
    if READONLY:
        log.info("READ-ONLY mode: content from %s, all writes disabled", CONTENT)
    else:
        seed_content()
        threading.Thread(target=history_watcher, name="history", daemon=True).start()
    log.info("content: %s, pages: %s, port %d, editor password: %s",
             CONTENT, PAGES, PORT, "n/a (read-only)" if READONLY
             else "yes" if EDITOR_PASSWORD else "NO (H6082_EDITOR_PASSWORD is not set)")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
