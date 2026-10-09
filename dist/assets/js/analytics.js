/* Google Analytics 4. So carrega depois do aceite de cookies (LGPD); recusar mantem o GA desligado.
   O ID vem de assets/js/config.js (ACROPOLE_CONFIG.analytics). */
(function(){
  var started=false,id="";
  function cfg(){
    var c=(window.ACROPOLE_CONFIG||{}).analytics||{};
    id=c.id||"";
    return c.provider==="ga4"&&/^G-[A-Z0-9]+$/.test(id);
  }
  function start(){
    if(started||!cfg())return;started=true;
    window["ga-disable-"+id]=false;
    var dl=window.dataLayer=window.dataLayer||[];
    window.gtag=function(){dl.push(arguments)};
    gtag("consent","default",{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"granted"});
    gtag("js",new Date());
    gtag("config",id,{allow_google_signals:false,allow_ad_personalization_signals:false});
    var s=document.createElement("script");s.async=true;
    s.src="https://www.googletagmanager.com/gtag/js?id="+encodeURIComponent(id);
    document.head.appendChild(s);
  }
  function stop(){
    if(!cfg())return;
    window["ga-disable-"+id]=true;
    if(window.gtag)gtag("consent","update",{analytics_storage:"denied"});
  }
  function check(){
    var v=window.AcropoleConsent&&window.AcropoleConsent.get();
    if(v==="accepted")start();
  }
  window.addEventListener("acropole:consent",function(e){
    if(e.detail==="accepted")start();else stop();
  });
  if(document.readyState==="complete")check();else document.addEventListener("DOMContentLoaded",check);
})();
