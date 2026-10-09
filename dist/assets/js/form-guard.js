/* Camada extra contra envios automatizados. Não altera o formulário nem a validação:
   apenas registra há quantos segundos a página estava aberta quando o envio ocorreu.
   Robôs costumam enviar em menos de 3 segundos; o n8n pode descartar esses casos. */
(function(){
  var t0=Date.now();
  function stamp(f){
    var i=f.querySelector('input[name="tempo_preenchimento_s"]');
    if(!i){i=document.createElement("input");i.type="hidden";i.name="tempo_preenchimento_s";f.appendChild(i);}
    i.value=String(Math.round((Date.now()-t0)/1000));
  }
  document.addEventListener("submit",function(e){
    var f=e.target;
    if(f&&f.matches&&f.matches("form[data-endpoint-form]")){try{stamp(f);}catch(_){}}
  },true);
})();
