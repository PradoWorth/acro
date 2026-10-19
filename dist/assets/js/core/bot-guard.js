/* Proteção anti-robô (Cloudflare Turnstile). Fica desligada enquanto
   ACROPOLE_CONFIG.turnstile.siteKey estiver vazio: nada é carregado e nada muda.
   Quando ligada, gera um token por envio e o anexa ao lead como "cf_turnstile".
   O token só vale se o n8n o validar no servidor (ver n8n-validar-lead.js). */
(function(){
  var cfg=((window.ACROPOLE_CONFIG||{}).turnstile)||{};
  var key=cfg.siteKey;
  if(!key)return;
  var token="",wid=null,waiters=[],box=null,busy=false;

  function settle(t){
    token=t||"";
    var w=waiters;waiters=[];
    w.forEach(function(f){try{f(token)}catch(_){}});
  }
  function renew(){
    if(!window.turnstile||wid===null)return;
    token="";
    try{window.turnstile.reset(wid)}catch(_){}
  }
  function take(){var t=token;token="";setTimeout(renew,300);return t}
  function wait(ms){
    return new Promise(function(res){
      if(token){res(take());return}
      var done=false,to=setTimeout(function(){if(!done){done=true;res("")}},ms||6000);
      waiters.push(function(t){if(done)return;done=true;clearTimeout(to);res(t?take():"")});
    });
  }
  window.__acTsToken=function(){return take()};
  window.__acTsWait=function(){renew();return wait(8000)};

  function render(){
    if(wid!==null||!window.turnstile)return;
    box=document.createElement("div");
    box.setAttribute("aria-hidden","true");
    document.body.appendChild(box);
    wid=window.turnstile.render(box,{
      sitekey:key,
      action:cfg.action||"lead",
      appearance:"interaction-only",
      "refresh-expired":"auto",
      callback:function(t){settle(t)},
      "error-callback":function(){settle("")},
      "expired-callback":function(){token=""}
    });
  }
  function load(){
    if(window.turnstile){render();return}
    var s=document.createElement("script");
    s.src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async=true;s.defer=true;
    s.onload=render;
    document.head.appendChild(s);
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",load);else load();

  function stamp(f,t){
    var i=f.querySelector('input[name="cf_turnstile"]');
    if(!i){i=document.createElement("input");i.type="hidden";i.name="cf_turnstile";f.appendChild(i)}
    i.value=t||"";
  }
  document.addEventListener("submit",function(e){
    var f=e.target;
    if(!f||!f.matches||!f.matches("form[data-endpoint-form]")||busy)return;
    if(token){stamp(f,take());return}
    e.preventDefault();e.stopImmediatePropagation();
    busy=true;
    wait(6000).then(function(t){
      stamp(f,t);busy=false;
      try{f.requestSubmit()}catch(_){f.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))}
    });
  },true);
})();
