(function(){
  var root=document.querySelector('[data-cityfinder]');if(!root)return;
  var input=root.querySelector('input[type=text]'),list=root.querySelector('.cf__list'),btn=root.querySelector('[data-cf-check]'),res=root.querySelector('.cf__res'),next=root.querySelector('[data-cf-next]'),wrap=document.getElementById('cf-form');
  var DATA=null,loading=null,chosen=null,idx=-1,LIMIT=50000;
  function norm(s){return String(s).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim()}
  function fmt(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'.')}
  function load(){
    if(DATA)return Promise.resolve(DATA);
    if(window.ACROPOLE_MUN){DATA=prep(window.ACROPOLE_MUN);return Promise.resolve(DATA)}
    if(!loading)loading=fetch(root.getAttribute('data-src'),{credentials:'same-origin'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){DATA=prep(j.d);return DATA});
    return loading;
  }
  function prep(d){return d.map(function(r){return{n:r[0],u:r[1],p:r[2],k:norm(r[0])}})}
  function show(html,cls){res.className='cf__res'+(cls?' cf__res--'+cls:'');res.innerHTML=html;res.hidden=false}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function closeList(){list.hidden=true;list.innerHTML='';idx=-1;input.setAttribute('aria-expanded','false')}
  function suggest(){
    var q=norm(input.value);chosen=null;hideForm();
    if(q.length<2){closeList();res.hidden=true;return}
    load().then(function(D){
      var a=[],b=[];
      for(var i=0;i<D.length&&a.length<30;i++){var k=D[i].k;if(k.indexOf(q)===0)a.push(D[i]);else if(k.indexOf(' '+q)>-1)b.push(D[i])}
      var m=a.concat(b).slice(0,8);
      if(!m.length){closeList();return}
      list.innerHTML=m.map(function(r,j){return '<li role="option" id="cf-o'+j+'" data-i="'+D.indexOf(r)+'">'+esc(r.n)+' <span>'+r.u+'</span></li>'}).join('');
      list.hidden=false;idx=-1;input.setAttribute('aria-expanded','true');
    }).catch(function(){closeList()});
  }
  function pick(r){chosen=r;input.value=r.n+' ('+r.u+')';closeList();check()}
  function hideForm(){if(wrap){wrap.hidden=true}if(next)next.hidden=true}
  function check(){
    var q=norm(input.value.replace(/\s*\([a-z]{2}\)\s*$/i,''));
    if(!q){show('Digite o nome da cidade onde o imóvel está.','warn');return}
    load().then(function(D){
      var r=chosen;
      if(!r){
        var m=D.filter(function(x){return x.k===q});
        if(m.length===1)r=m[0];
        else if(m.length>1){show('Há mais de uma cidade com esse nome. Escolha na lista a que corresponde ao seu imóvel, com o estado.','warn');suggest();return}
        else{show('Não encontramos essa cidade. Confira a grafia e escolha uma opção da lista que aparece ao digitar.','warn');return}
      }
      chosen=r;
      var near=Math.abs(r.p-LIMIT)<=2000;
      if(r.p>LIMIT){
        show('<strong>'+esc(r.n)+' ('+r.u+') atende ao critério de localização.</strong> A cidade tem '+fmt(r.p)+' habitantes (IBGE, Censo 2022), acima de 50 mil.'+(near?' O número está próximo do limite, então a conferência final será feita na análise.':'')+' Aprovação, valor e condições dependem da análise do imóvel, da documentação e da instituição financeira.','ok');
        if(next)next.hidden=false;
        var c=document.getElementById('q-cidade');if(c){c.value=r.n+' ('+r.u+')'}
      }else{
        hideForm();
        show('<strong>'+esc(r.n)+' ('+r.u+') não atende ao critério de localização.</strong> A cidade tem '+fmt(r.p)+' habitantes (IBGE, Censo 2022) e o imóvel precisa estar em município com mais de 50 mil.'+(near?' O número está próximo do limite, mas o critério é aplicado como está.':'')+' Se o imóvel que pretende oferecer estiver em outra cidade, digite o nome dela acima.','no');
      }
    }).catch(function(){show('Não foi possível consultar a lista agora. Tente novamente ou chame no WhatsApp.','warn')});
  }
  input.addEventListener('input',suggest);
  input.addEventListener('keydown',function(e){
    var li=list.querySelectorAll('li');
    if(e.key==='ArrowDown'&&li.length){e.preventDefault();idx=(idx+1)%li.length}
    else if(e.key==='ArrowUp'&&li.length){e.preventDefault();idx=(idx-1+li.length)%li.length}
    else if(e.key==='Enter'){e.preventDefault();if(idx>-1&&li[idx]){pick(DATA[+li[idx].getAttribute('data-i')])}else{closeList();check()}return}
    else if(e.key==='Escape'){closeList();return}
    else return;
    li.forEach(function(x,j){x.setAttribute('aria-selected',j===idx?'true':'false')});
    input.setAttribute('aria-activedescendant',idx>-1?li[idx].id:'');
  });
  input.addEventListener('focus',function(){load().catch(function(){})},{once:true});
  list.addEventListener('mousedown',function(e){var li=e.target.closest('li');if(li){e.preventDefault();pick(DATA[+li.getAttribute('data-i')])}});
  document.addEventListener('click',function(e){if(!root.contains(e.target))closeList()});
  btn.addEventListener('click',function(){closeList();check()});
  if(next)next.addEventListener('click',function(){if(!wrap)return;wrap.hidden=false;next.hidden=true;var c=document.getElementById('q-cidade');if(chosen&&c){c.value=chosen.n+' ('+chosen.u+')'}wrap.scrollIntoView({behavior:'smooth',block:'start'});var f=wrap.querySelector('select');if(f)setTimeout(function(){f.focus({preventScroll:true})},400)});
  // mensagem do WhatsApp com a cidade e o tipo de imóvel
  var form=wrap&&wrap.querySelector('form');
  if(form)form.addEventListener('submit',function(){
    var g=function(n){var e=form.elements[n];return e?e.value:''};
    var t='Oi, sou '+g('nome')+'. Tenho um imóvel ('+g('tipo_imovel')+') em '+g('cidade')+' e quero conferir as condições para uma análise de crédito com garantia de imóvel. Vi na página de cidades da Acrópole Capital.';
    form.setAttribute('data-whatsapp-redirect','https://wa.me/5543984321492?text='+encodeURIComponent(t));
  },true);
})();
