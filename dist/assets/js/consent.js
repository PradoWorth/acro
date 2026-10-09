/* Consentimento de cookies (LGPD). Guarda a decisão do visitante, mostra o aviso
   enquanto não houver decisão e avisa o resto do site quando ela muda.
   Aceitar: libera o cookie de atribuição de campanha (30 dias) e o Consent Mode.
   Recusar: nada além do essencial; a origem da visita fica só nesta sessão. */
(function(){
  var KEY="cookieconsent:v1",bar=null,last=null;
  function get(){try{var v=localStorage.getItem(KEY);return v==="accepted"||v==="rejected"?v:null}catch(e){return null}}
  function gtag(){window.dataLayer.push(arguments)}
  function gtagUpdate(v){
    try{
      window.dataLayer=window.dataLayer||[];
      var g=v==="accepted"?"granted":"denied";
      gtag("consent","update",{ad_storage:g,ad_user_data:g,ad_personalization:g,analytics_storage:g});
      window.dataLayer.push({event:"consent_update",consent_state:v});
    }catch(e){}
  }
  function dropAttribution(){
    try{document.cookie="app_attribution=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax"+(location.protocol==="https:"?"; Secure":"")}catch(e){}
  }
  function setH(){
    if(!bar)return;
    var h=bar.getAttribute("data-show")==="true"?bar.offsetHeight+12:0;
    document.documentElement.style.setProperty("--cookiebar-h",h+"px");
  }
  function show(on){
    if(!bar)return;
    bar.setAttribute("data-show",on?"true":"false");
    setH();
    if(on){window.addEventListener("resize",setH)}else{window.removeEventListener("resize",setH)}
  }
  function set(v){
    if(v!=="accepted"&&v!=="rejected")return;
    try{localStorage.setItem(KEY,v)}catch(e){}
    if(v==="rejected")dropAttribution();
    gtagUpdate(v);
    show(false);
    if(last&&last.focus){try{last.focus()}catch(e){}}
    last=null;
    try{window.dispatchEvent(new CustomEvent("acropole:consent",{detail:v}))}catch(e){}
  }
  function open(trigger){
    if(!bar)return;
    last=trigger||null;
    show(true);
    var b=bar.querySelector("[data-cookie-accept]");
    if(b&&trigger){try{b.focus()}catch(e){}}
  }
  window.AcropoleConsent={get:get,set:set,open:open};
  function init(){
    bar=document.getElementById("cookiebar");
    if(bar){
      var a=bar.querySelector("[data-cookie-accept]"),r=bar.querySelector("[data-cookie-reject]");
      if(a)a.addEventListener("click",function(){set("accepted")});
      if(r)r.addEventListener("click",function(){set("rejected")});
      bar.addEventListener("keydown",function(e){if(e.key==="Escape"&&get()){show(false)}});
      if(!get())requestAnimationFrame(function(){show(true)});
    }
    document.addEventListener("click",function(e){
      var t=e.target.closest&&e.target.closest("[data-cookie-open]");
      if(t){e.preventDefault();open(t)}
    });
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
