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
  bar.addEventListener("click",function(){
    var dl=window.dataLayer=window.dataLayer||[];
    var d={page_path:location.pathname,placement:"top_bar",cta_target:bar.getAttribute("href")||"",viewport:window.innerWidth<768?"mobile":"desktop"};
    var o={event:"announcement_click"},k;for(k in d)o[k]=d[k];dl.push(o);
    if(typeof window.gtag==="function")window.gtag("event","announcement_click",d);
  },true);
  var mq=window.matchMedia("(max-width: 47.99rem)"),tick=false,pt=document.querySelector(".partners");
  function past(){
    var y=window.pageYOffset||0;
    if(pt){return pt.getBoundingClientRect().top<=window.innerHeight*.75}
    return y>window.innerHeight*.9;
  }
  function upd(){
    tick=false;
    if(mq.matches&&past()){root.classList.add("annbar-hide")}else{root.classList.remove("annbar-hide")}
  }
  window.addEventListener("scroll",function(){if(!tick){tick=true;window.requestAnimationFrame(upd)}},{passive:true});
  window.addEventListener("resize",upd,{passive:true});
  var mqf=function(){if(!mq.matches)root.classList.remove("annbar-hide")};
  if(mq.addEventListener)mq.addEventListener("change",mqf);
})();
