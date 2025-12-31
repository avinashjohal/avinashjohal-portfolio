document.addEventListener("DOMContentLoaded",()=>{
  const buttons=document.querySelectorAll(".filters .btn");
  const cards=document.querySelectorAll("#projectGrid .project");
  buttons.forEach(btn=>{
    btn.addEventListener("click",()=>{
      const f=btn.dataset.filter;
      buttons.forEach(b=>b.classList.remove("active"));
      btn.classList.add("active");
      cards.forEach(c=>{
        if(f==="all"){c.style.display="";return}
        const tags=(c.dataset.tags||"").split(",");
        c.style.display=tags.includes(f)?"":"none";
      });
    });
  });
});

