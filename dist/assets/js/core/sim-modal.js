/* Abre o Simulador Home Equity em janela (iframe do mesmo domínio).
   Acessível: foco preso na janela (o resto da página fica inerte), Esc fecha
   e o foco volta para o botão que abriu. */
(function(){
  var last=null,ov=null,bd=null,inerted=[];
  function close(){
    if(!ov)return;
    document.documentElement.classList.remove("sim-open");
    inerted.forEach(function(el){el.inert=false;el.removeAttribute("aria-hidden")});
    inerted=[];
    ov.remove();ov=null;
    if(bd){bd.remove();bd=null}
    document.removeEventListener("keydown",key);
    if(last&&last.focus){try{last.focus()}catch(e){}}
  }
  function key(e){if(e.key==="Escape")close()}
  function open(trigger){
    if(ov)return;last=trigger;
    var base=(trigger.getAttribute("data-sim-src")||"/simulador-home-equity").split("?")[0];
    ov=document.createElement("div");
    ov.className="simmodal";
    ov.setAttribute("role","dialog");
    ov.setAttribute("aria-modal","true");
    ov.setAttribute("aria-labelledby","simmodal-title");
    ov.innerHTML='<span class="sr" tabindex="0" data-sim-edge="start"></span><div class="simmodal__bar"><span id="simmodal-title">Simulador Home Equity</span><button type="button" class="simmodal__close" aria-label="Fechar simulador"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13"/></svg></button></div><iframe class="simmodal__frame" title="Simulador Home Equity" src="'+base+'?embed=1"></iframe><span class="sr" tabindex="0" data-sim-edge="end"></span>';
    Array.prototype.forEach.call(document.body.children,function(el){
      if(!el.inert&&el.tagName!=="SCRIPT"){el.inert=true;el.setAttribute("aria-hidden","true");inerted.push(el)}
    });
    bd=document.createElement("div");bd.className="simmodal__backdrop";bd.addEventListener("click",close);
    document.body.appendChild(bd);
    document.body.appendChild(ov);
    requestAnimationFrame(function(){if(bd)bd.setAttribute("data-show","true")});
    document.documentElement.classList.add("sim-open");
    ov.querySelector(".simmodal__close").addEventListener("click",close);
    /* Bordas da janela: o foco que sai pelo fim volta ao botão de fechar e o que
       sai pelo começo (Shift+Tab) volta para dentro do simulador. */
    ov.querySelector('[data-sim-edge="end"]').addEventListener("focus",function(){ov.querySelector(".simmodal__close").focus()});
    ov.querySelector('[data-sim-edge="start"]').addEventListener("focus",function(){ov.querySelector(".simmodal__frame").focus()});
    document.addEventListener("keydown",key);
    ov.querySelector(".simmodal__close").focus();
  }
  document.addEventListener("click",function(e){
    var t=e.target.closest&&e.target.closest("[data-sim-open]");if(!t)return;
    if(e.metaKey||e.ctrlKey||e.shiftKey||e.button===1)return;
    e.preventDefault();open(t);
  });
  /* O simulador pode pedir para fechar a janela (ex.: depois de abrir o WhatsApp). */
  window.addEventListener("message",function(e){
    if(e.origin!==location.origin)return;
    if(e.data&&e.data.type==="acropole:sim-close")close();
  });
})();

/* Faixa de anuncio: evento de clique para o GA4 (so chega ao Google com cookies aceitos)
   e, no celular, esconde ao rolar para baixo e volta ao rolar para cima. */
(function(){
  var bar=document.querySelector(".annbar");if(!bar)return;
  var root=document.documentElement;
  if(!bar.classList.contains("annbar--static"))bar.addEventListener("click",function(){
    var dl=window.dataLayer=window.dataLayer||[];
    var d={page_path:location.pathname,placement:"top_bar",cta_target:bar.getAttribute("href")||"",viewport:window.innerWidth<768?"mobile":"desktop"};
    var o={event:"announcement_click"},k;for(k in d)o[k]=d[k];dl.push(o);
    if(typeof window.gtag==="function")window.gtag("event","announcement_click",d);
  },true);
  var mq=window.matchMedia("(max-width: 47.99rem)"),tick=false,pt=document.querySelector(".partners");
  function past(){
    if(bar.classList.contains("annbar--static"))return false;
    var y=window.pageYOffset||0;
    if(pt){return pt.getBoundingClientRect().top<=window.innerHeight*.75}
    return y>window.innerHeight*.9;
  }
  function upd(){
    tick=false;
    if(root.classList.contains("is-typing"))return;
    if(past()){root.classList.add("annbar-hide")}else{root.classList.remove("annbar-hide")}
  }
  window.addEventListener("scroll",function(){if(!tick){tick=true;window.requestAnimationFrame(upd)}},{passive:true});
  window.addEventListener("resize",upd,{passive:true});
})();

/* Abrir o simulador a partir do menu lateral: fecha o menu antes. */
document.addEventListener("click",function(e){
  var t=e.target.closest&&e.target.closest(".drawer [data-sim-open]");if(!t)return;
  var c=document.querySelector(".drawer [data-drawer-close]");if(c)c.click();
},true);

/* Card do menu lateral: as mensagens viram a cada 4 s enquanto o menu esta aberto. */
(function(){
  var dr=document.getElementById("drawer"),box=document.querySelector(".drawer__sim__t");if(!dr||!box)return;
  var items=box.querySelectorAll(".rot"),i=0,timer=null,reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(items.length<2)return;
  function show(n){
    var prev=items[i];i=n;
    prev.classList.remove("is-on");prev.classList.add("is-out");
    setTimeout(function(){prev.classList.remove("is-out")},800);
    items[i].classList.add("is-on");
  }
  function reset(){Array.prototype.forEach.call(items,function(el){el.classList.remove("is-on","is-out")});i=0;items[0].classList.add("is-on")}
  function start(){if(timer||reduce)return;timer=setInterval(function(){show((i+1)%items.length)},4000)}
  function stop(){if(timer){clearInterval(timer);timer=null}}
  function sync(){if(dr.getAttribute("data-open")==="true"){start()}else{stop();reset()}}
  if(window.MutationObserver)new MutationObserver(sync).observe(dr,{attributes:true,attributeFilter:["data-open"]});
  sync();
})();

/* Faixa de anuncio: as mensagens viram a cada 4 s; o botao fica fixo. */
(function(){
  var box=document.querySelector(".annbar__txt");if(!box)return;
  var items=box.querySelectorAll(".arot"),i=0,timer=null,root=document.documentElement;
  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(items.length<2||reduce)return;
  var bar=document.querySelector(".annbar"),paused=false;
  if(bar){["mouseenter","focusin","touchstart"].forEach(function(t){bar.addEventListener(t,function(){paused=true},{passive:true})});["mouseleave","focusout"].forEach(function(t){bar.addEventListener(t,function(){paused=false})})}
  function next(){
    if(paused||document.hidden||root.classList.contains("annbar-hide")||root.classList.contains("is-typing"))return;
    var prev=items[i];i=(i+1)%items.length;
    prev.classList.remove("is-on");prev.classList.add("is-out");
    setTimeout(function(){prev.classList.remove("is-out")},800);
    items[i].classList.add("is-on");
  }
  timer=setInterval(next,4000);
})();

/* Mede de onde vem cada abertura do simulador (faixa, menu, secao da home, etc.). */
document.addEventListener("click",function(e){
  var t=e.target.closest&&e.target.closest("[data-sim-open]");if(!t)return;
  var o=t.closest(".annbar")?"faixa":t.closest(".drawer")?"menu_mobile":t.closest(".megapanel")?"menu_desktop":t.closest("#home-equity")?"secao_home":"pagina";
  var d={page_path:location.pathname,origin:o,viewport:window.innerWidth<768?"mobile":"desktop"};
  var dl=window.dataLayer=window.dataLayer||[],x={event:"simulator_open"},k;for(k in d)x[k]=d[k];dl.push(x);
  if(typeof window.gtag==="function")window.gtag("event","simulator_open",d);
},true);

/* Campo em foco (teclado aberto no celular): o menu sobe para nao ficar solto no meio da tela.
   Se a pessoa rolar a pagina de volta ao topo com o campo ainda em foco, o menu volta. */
(function(){
  var root=document.documentElement,t=0,focused=false,mq=window.matchMedia("(max-width: 47.99rem)"),raf=0;
  function f(e){var n=e.target&&e.target.tagName;return n==="INPUT"||n==="SELECT"||n==="TEXTAREA"}
  function apply(){raf=0;var ae=document.activeElement,inp=!!ae&&/^(INPUT|SELECT|TEXTAREA)$/.test(ae.tagName),top=(window.pageYOffset||0)<160;if(focused&&!inp)focused=false;root.classList.toggle("is-typing",focused&&inp&&!top)}
  document.addEventListener("focusin",function(e){if(!f(e))return;clearTimeout(t);focused=true;apply()});
  document.addEventListener("focusout",function(e){if(!f(e))return;clearTimeout(t);t=setTimeout(function(){focused=false;root.classList.remove("is-typing")},400)});
  window.addEventListener("scroll",function(){if(focused&&!raf)raf=requestAnimationFrame(apply)},{passive:true});
})();

/* Modo TV (acropolecapital.com.br/?tv): tela sempre ligada e sem avisos sobrepostos, para deixar o site aberto o dia todo. */
(function(){
  if(!/[?&]tv(=1|=true)?(&|$)/.test(location.search))return;
  document.documentElement.classList.add("is-tv");
  var lock=null;
  function ask(){if(!("wakeLock" in navigator)||document.hidden)return;navigator.wakeLock.request("screen").then(function(l){lock=l;l.addEventListener("release",function(){lock=null})}).catch(function(){})}
  ask();document.addEventListener("visibilitychange",function(){if(!document.hidden&&!lock)ask()});
})();
