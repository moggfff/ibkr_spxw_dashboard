async function action(cmd){
  const res = await fetch('/api/'+cmd);
  const data = await res.json();
  document.getElementById('status').innerText = data.message || JSON.stringify(data);
  if(data.signals){ document.getElementById('signals').innerText = data.signals.join('\n'); }
}
