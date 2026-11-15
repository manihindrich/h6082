# h6082
![h6082: markdown homepage](/media/h6082-hero.cs.svg)

---
#50%
## h6082 **markdown homepage ušitá na míru**
**Startovní stránka, která se píše jako poznámky.**
Každá záložka je jeden soubor `content/pages/*.md`. Upravíš ho ve svém editoru, nebo rovnou tady v prohlížeči s živým náhledem. Uložíš a je to venku, žádné nasazování.

`#` založí sloupec, `##` kartu a do ní patří odkazy, úkoly, poznámky, stav služeb nebo RSS. Funkcí postupně přibývá.
/

**Bez databáze, bez buildu, bez sledování.**
Vzhled se ladí v jednom přehledném TOML souboru. Celé to běží v jediném úsporném kontejneru, takže nároky na hardware jsou skromné. Stačí i ta pověstná brambora. Prohlížeč nic nestahuje z cizích serverů, tvá data zůstávají u tebe.

#25%
## Dokumentace a konfigurace {.fill}
{{files system}}

#25%
## Autor a aplikace {.fill}
<div class="author" markdown="1">
<div class="author-avatar"><img src="/static/img/author.webp" width="52" height="52" alt="" decoding="async"></div>
<div class="author-body" markdown="1">
<span class="author-name">Mani Hindrich</span>
<span class="author-role">{{email mani hindrich.cz}}</span>
<div class="author-links" markdown="1">
[code.nolog.cz/hindrich/h6082](https://code.nolog.cz/hindrich/h6082) [github.com/manihindrich/h6082](https://github.com/manihindrich/h6082)
</div>
</div>
</div>
/
| | |
|---|---|
| verze | **1.0** |
| licence | [GPL-3.0](https://code.nolog.cz/hindrich/h6082/src/branch/master/LICENSE) · třetí strany [?](JetBrains Mono — OFL-1.1\nPython-Markdown — BSD-3-Clause\nPyMdown Extensions — MIT\nPygments — BSD-2-Clause\ndefusedxml — PSF-2.0) |

---
//
#-
#+
## Soubory
{{files user}}
/
### Nový soubor
{{newfile}}


#
## 🕓 Poslední změny
{{history 5 auto}}

<small>Všechny verze souboru najdeš v editoru pod **historie**, s diffem a obnovením.</small>


#
##* 📊 Server
{{sys cpu cpuinfo mem swap load procs io temp disk uptime auto}}


#-