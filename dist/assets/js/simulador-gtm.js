/* Google Tag Manager (servidor de tags da Acrópole) com Consent Mode v2.
   Padrão: armazenamento de anúncios e de análise NEGADO até o visitante aceitar
   no aviso de cookies. Com a decisão salva (mesmo domínio), o estado é aplicado
   antes do GTM carregar; mudanças posteriores chegam pelo evento do aviso ou,
   dentro da janela do site, pelo evento "storage" do navegador. */
(function(w,d){
  /* Aberto dentro da janela do site (?embed=1): o aviso de cookies fica com o site. */
  if(/[?&]embed=1\b/.test(location.search))d.documentElement.classList.add("is-embed");
  var KEY="cookieconsent:v1";
  w.dataLayer=w.dataLayer||[];
  function gtag(){w.dataLayer.push(arguments)}
  function state(){try{return localStorage.getItem(KEY)}catch(e){return null}}
  function g(v){return v==="accepted"?"granted":"denied"}
  var c=g(state());
  gtag("consent","default",{ad_storage:c,ad_user_data:c,ad_personalization:c,analytics_storage:c,functionality_storage:"granted",security_storage:"granted",wait_for_update:500});
  gtag("set","ads_data_redaction",c!=="granted");
  function update(v){var x=g(v);gtag("consent","update",{ad_storage:x,ad_user_data:x,ad_personalization:x,analytics_storage:x});gtag("set","ads_data_redaction",x!=="granted")}
  w.addEventListener("acropole:consent",function(e){update(e.detail)});
  w.addEventListener("storage",function(e){if(e.key===KEY)update(e.newValue)});
  (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src="https://load.sst.acropolecapital.com.br/6jiqvdkzns.js?"+i;f.parentNode.insertBefore(j,f);})(w,d,'script','dataLayer','8=GgpHLDA7XDlEXSkxLkRETwVTSEVVUBUHTg8ZGQsGHgUWDRsbDQIQBV0NFQZKFAM%3D');
})(window,document);
