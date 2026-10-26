(function(){
  var dl=window.dataLayer=window.dataLayer||[];
  /* Caminho limpo da página, sem barra final e sem .html: "agronegocio/custeio-agricola", "home". */
  var path=(location.pathname||"/").replace(/\.html$/,"").replace(/\/index$/,"").replace(/^\/+|\/+$/g,"")||"home";
  var type=path==="home"?"home":(path.indexOf("/")>0?path.split("/")[0]:"pagina");
  function push(ev,data){var o={event:ev,page_path:location.pathname,page_clean:path,page_type:type},k;for(k in data)o[k]=data[k];dl.push(o);
    if(typeof window.gtag==="function"){var q={};for(k in o){if(k!=="event")q[k]=o[k];}window.gtag("event",ev,q);}}
  /* Onde na página o clique aconteceu: a seção mais próxima (id, ou a classe da faixa). */
  function where(el){
    var s=el.closest&&el.closest("section,header,footer,nav,aside");
    if(!s)return"pagina";
    if(s.id)return s.id;
    if(s.tagName==="HEADER"||s.classList.contains("mast"))return"cabecalho";
    if(s.tagName==="FOOTER")return"rodape";
    return(s.className||s.tagName).toString().replace(/\s+/g," ").trim().slice(0,30);
  }
  function fname(f){return f.getAttribute("data-form")||"form"}
  document.addEventListener("click",function(e){
    var a=e.target.closest&&e.target.closest("a,button");if(!a)return;
    var href=a.getAttribute("href")||"";
    if(/wa\.me|api\.whatsapp\.com/.test(href)){push("whatsapp_click",{link_url:href.split("?")[0],cta_location:where(a)});}
    else if(/^tel:/i.test(href)){push("phone_click",{cta_location:where(a)});}
    else if(/^mailto:/i.test(href)){push("email_click",{cta_location:where(a)});}
    if(a.hasAttribute("data-lead-modal")||a.hasAttribute("data-cta")||(a.classList.contains("btn")&&a.closest(".ctaband"))){
      push("cta_click",{cta_text:(a.textContent||"").replace(/\s+/g," ").trim().slice(0,60),cta_target:href,cta_location:where(a)});
    }
  },true);
  document.addEventListener("focusin",function(e){
    var f=e.target.closest&&e.target.closest("form[data-endpoint-form]");
    if(f&&!f.__seoStarted){f.__seoStarted=1;push("form_start",{form_name:fname(f),form_location:where(f)});}
  });
  document.addEventListener("submit",function(e){
    var f=e.target;if(!f||!f.matches)return;
    if(f.matches("form[data-endpoint-form]")){push("form_submit_attempt",{form_name:fname(f),form_location:where(f)});}
    else if(f.closest&&f.closest(".toolcard")){push("calculator_use",{tool_name:path});}
  },true);
  function watch(){
    var forms=document.querySelectorAll("form[data-endpoint-form]");
    Array.prototype.forEach.call(forms,function(f){
      var ok=f.querySelector(".formstate--ok"),er=f.querySelector(".formstate--err");
      if(ok&&!ok.__seoWatch&&window.MutationObserver){ok.__seoWatch=1;
        new MutationObserver(function(){
          if(ok.getAttribute("data-show")==="true"){push("generate_lead",{form_name:fname(f),form_location:where(f),lead_origin:(f.querySelector('[name="origem_pagina"]')||{}).value||path});}
        }).observe(ok,{attributes:true,attributeFilter:["data-show"]});}
      if(er&&!er.__seoWatch&&window.MutationObserver){er.__seoWatch=1;
        new MutationObserver(function(){
          if(er.getAttribute("data-show")==="true"){push("form_error",{form_name:fname(f),form_location:where(f)});}
        }).observe(er,{attributes:true,attributeFilter:["data-show"]});}
    });
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",watch);else watch();
})();
