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
