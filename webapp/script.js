document.addEventListener('DOMContentLoaded', () => {
    const circuitDescription = document.getElementById('circuitDescription');
    const proceedBtn = document.getElementById('proceedBtn');
    const resetBtn = document.getElementById('resetBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const shareBtn = document.getElementById('shareBtn');
    const resultsGrid = document.getElementById('resultsGrid');
    const truthTable = document.getElementById('truthTable');
    const circuitDiagram = document.getElementById('circuitDiagram');
    const verilogCode = document.getElementById('verilogCode');
    const testbenchCode = document.getElementById('testbenchCode');
    const loadingOverlay = document.getElementById('loadingOverlay');
  
    particlesJS('particles-js', {
      particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: "#ffffff" },
        shape: { type: "circle" },
        opacity: { value: 0.5, random: true, anim: { enable: true, speed: 1, opacity_min: 0.1, sync: false } },
        size: { value: 3, random: true, anim: { enable: false, speed: 40, size_min: 0.1, sync: false } },
        line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
        move: { enable: true, speed: 6, direction: "none", random: false, straight: false, out_mode: "out", bounce: false }
      },
      interactivity: {
        detect_on: "canvas",
        events: { onhover: { enable: true, mode: "repulse" }, onclick: { enable: true, mode: "push" }, resize: true },
        modes: { grab: { distance: 400, line_linked: { opacity: 1 } }, bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 }, repulse: { distance: 200, duration: 0.4 }, push: { particles_nb: 4 }, remove: { particles_nb: 2 } }
      },
      retina_detect: true
    });
  
    proceedBtn.addEventListener('click', async () => {
      const description = circuitDescription.value.trim();
      if (!description) {
        alert('Please enter a circuit description.');
        return;
      }
  
      loadingOverlay.style.display = 'flex';
      proceedBtn.disabled = true;
  
      try {
        const response = await fetch('https://text-to-verilog-generator.onrender.com/verilogify', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ description })
        });
  
        if (!response.ok) {
          throw new Error('API request failed');
        }
  
        const data = await response.json();
  
        // Populate Truth Table
        let tableHtml = '<table><tr>';
        const keys = Object.keys(data.final_table);
        keys.forEach(key => {
          tableHtml += `<th>${key}</th>`;
        });
        tableHtml += '</tr>';
        
        const rowCount = data.final_table[keys[0]].length;
        for (let i = 0; i < rowCount; i++) {
          tableHtml += '<tr>';
          keys.forEach(key => {
            tableHtml += `<td>${data.final_table[key][i]}</td>`;
          });
          tableHtml += '</tr>';
        }
        tableHtml += '</table>';
        truthTable.innerHTML = tableHtml;
  
        // Load Circuit Diagram
        circuitDiagram.innerHTML = `<img src="${data.diagram}" alt="Circuit Diagram" style="max-width:100%;height:auto;">`;
  
        // Display Verilog Code
        verilogCode.innerHTML = `<pre><code class="verilog">${data.verilog_code}</code></pre>`;
  
        // Display Testbench Code
        testbenchCode.innerHTML = `<pre><code class="verilog">${data.testbench_code}</code></pre>`;
  
        hljs.highlightAll();
  
        resultsGrid.style.display = 'grid';
        resetBtn.style.display = 'inline-block';
        downloadBtn.style.display = 'inline-block';
        shareBtn.style.display = 'inline-block';
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing your request. Please try again.');
      } finally {
        loadingOverlay.style.display = 'none';
        proceedBtn.disabled = false;
      }
    });
  
    resetBtn.addEventListener('click', () => {
      circuitDescription.value = '';
      resultsGrid.style.display = 'none';
      resetBtn.style.display = 'none';
      downloadBtn.style.display = 'none';
      shareBtn.style.display = 'none';
      truthTable.innerHTML = '';
      circuitDiagram.innerHTML = '';
      verilogCode.innerHTML = '';
      testbenchCode.innerHTML = '';
    });
  
    downloadBtn.addEventListener('click', async () => {
      const zip = new JSZip();
      zip.file("truth_table.txt", truthTable.innerText);
      zip.file("verilog_code.v", verilogCode.innerText);
      zip.file("testbench_code.v", testbenchCode.innerText);
      
      const imgSrc = circuitDiagram.querySelector('img').src;
      const imgResponse = await fetch(imgSrc);
      const imgBlob = await imgResponse.blob();
      zip.file("circuit_diagram.png", imgBlob);
  
      const content = await zip.generateAsync({type:"blob"});
      const link = document.createElement("a");
      link.href = URL.createObjectURL(content);
      link.download = "verilog_generator_output.zip";
      link.click();
    });
  
    shareBtn.addEventListener('click', () => {
      const shareUrl = window.location.href + '?description=' + encodeURIComponent(circuitDescription.value);
      navigator.clipboard.writeText(shareUrl).then(() => {
        alert('Share URL copied to clipboard!');
      }).catch(err => {
        console.error('Error in copying text: ', err);
      });
    });
  
    document.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const targetElement = document.getElementById(targetId);
        const textToCopy = targetElement.innerText;
        
        navigator.clipboard.writeText(textToCopy).then(() => {
          btn.textContent = 'Copied!';
          setTimeout(() => {
            btn.textContent = 'Copy';
          }, 2000);
        }).catch(err => {
          console.error('Error in copying text: ', err);
        });
      });
    });
  
    // Check for shared URL
    const urlParams = new URLSearchParams(window.location.search);
    const sharedDescription = urlParams.get('description');
    if (sharedDescription) {
      circuitDescription.value = sharedDescription;
      proceedBtn.click();
    }
  });  