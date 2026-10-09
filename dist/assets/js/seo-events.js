(function(){
  var dl=window.dataLayer=window.dataLayer||[];
  function push(ev,data){var o={event:ev,page_path:location.pathname},k;for(k in data)o[k]=data[k];dl.push(o);}
  document.addEventListener("click",function(e){
    var a=e.target.closest&&e.target.closest("a,button");if(!a)return;
    var href=a.getAttribute("href")||"";
    if(/wa\.me|api\.whatsapp\.com/.test(href)){push("whatsapp_click",{link_url:href.split("?")[0]});}
    if(a.hasAttribute("data-lead-modal")||a.hasAttribute("data-cta")||(a.classList.contains("btn")&&a.closest(".ctaband"))){
      push("cta_click",{cta_text:(a.textContent||"").replace(/\s+/g," ").trim().slice(0,60),cta_target:href});
    }
  },true);
  document.addEventListener("focusin",function(e){
    var f=e.target.closest&&e.target.closest("form[data-endpoint-form]");
    if(f&&!f.__seoStarted){f.__seoStarted=1;push("form_start",{form_name:f.getAttribute("data-form")||"form"});}
  });
  document.addEventListener("submit",function(e){
    var f=e.target;
    if(f&&f.matches&&f.matches("form[data-endpoint-form]")){push("form_submit_attempt",{form_name:f.getAttribute("data-form")||"form"});}
  },true);
  function watch(){
    var forms=document.querySelectorAll("form[data-endpoint-form]");
    Array.prototype.forEach.call(forms,function(f){
      var ok=f.querySelector(".formstate--ok");if(!ok||ok.__seoWatch||!window.MutationObserver)return;ok.__seoWatch=1;
      new MutationObserver(function(){
        if(ok.getAttribute("data-show")==="true"){push("generate_lead",{form_name:f.getAttribute("data-form")||"form",lead_origin:(f.querySelector('[name="origem_pagina"]')||{}).value||""});}
      }).observe(ok,{attributes:true,attributeFilter:["data-show"]});
    });
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",watch);else watch();
})();
