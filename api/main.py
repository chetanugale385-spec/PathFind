<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PathFind AI - Smart Roadmap</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes pulse-bg {
            0%, 100% { background-color: rgba(30, 41, 59, 0.5); }
            50% { background-color: rgba(30, 41, 59, 0.8); }
        }
        .animate-loading { animation: pulse-bg 2s infinite; }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class="bg-[#0f172a] text-slate-200 font-sans min-h-screen">

    <div class="max-w-md mx-auto p-6">
        <header class="text-center mb-10 pt-6">
            <h1 class="text-4xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-blue-400 to-cyan-300">PathFind AI</h1>
            <p class="text-slate-500 text-[10px] mt-2 tracking-[0.3em] uppercase font-bold">ZCOER Student Project</p>
        </header>
        
        <div class="space-y-5">
            <div class="bg-slate-800/40 p-4 rounded-2xl border border-slate-700/50 shadow-inner">
                <label class="block text-[10px] font-bold text-blue-400 mb-2 uppercase tracking-widest">Select Branch</label>
                <select id="branch" class="w-full bg-transparent outline-none text-sm font-semibold appearance-none">
                    <option value="AIML" class="bg-slate-900">B.Tech AIML</option>
                    <option value="Computer" class="bg-slate-900">Computer Engineering</option>
                    <option value="IT" class="bg-slate-900">Information Technology</option>
                    <option value="ENTC" class="bg-slate-900">E&TC Engineering</option>
                </select>
            </div>

            <div class="bg-slate-800/40 p-4 rounded-2xl border border-slate-700/50 shadow-inner">
                <label class="block text-[10px] font-bold text-blue-400 mb-2 uppercase tracking-widest">Your Core Interest</label>
                <input type="text" id="interest" placeholder="e.g. Data Science, Web Dev" 
                       class="w-full bg-transparent outline-none text-sm placeholder:text-slate-600 font-semibold">
            </div>

            <button id="generate-btn" class="w-full py-5 bg-gradient-to-br from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 rounded-2xl font-black text-white shadow-xl shadow-blue-900/40 transition-all active:scale-[0.98]">
                GENERATE ROADMAP
            </button>
        </div>

        <div id="output-section" class="mt-12 hidden">
            <div class="flex items-center gap-3 mb-6 border-b border-slate-800 pb-4">
                <div class="w-3 h-3 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_12px_rgba(34,211,238,0.8)]"></div>
                <h2 class="text-lg font-bold text-white uppercase tracking-tight">AI Generated Path</h2>
            </div>
            
            <div id="roadmap-container" class="space-y-4 text-sm leading-relaxed">
                </div>
        </div>

        <footer class="text-center text-slate-700 text-[9px] mt-20 tracking-widest uppercase pb-10">
            © 2026 • Designed & Built by Chetan Ugale
        </footer>
    </div>

    <script>
        // Constant Vercel Endpoint
        const API_URL = "https://path-find-one.vercel.app/generate"; 

        document.getElementById('generate-btn').addEventListener('click', async () => {
            const branch = document.getElementById('branch').value;
            const interest = document.getElementById('interest').value;
            const btn = document.getElementById('generate-btn');
            const output = document.getElementById('output-section');
            const container = document.getElementById('roadmap-container');

            if (!interest.trim()) { 
                alert("Bhai, interest toh dalo!"); 
                return; 
            }

            // Start Loading
            btn.innerText = "PROCESSING...";
            btn.disabled = true;
            output.classList.remove('hidden');
            container.innerHTML = `
                <div class="p-8 bg-slate-800/30 border border-slate-700/50 rounded-3xl animate-loading">
                    <div class="h-3 bg-slate-700 rounded-full w-3/4 mb-5 animate-pulse"></div>
                    <div class="h-3 bg-slate-700 rounded-full w-full mb-5 animate-pulse"></div>
                    <div class="h-3 bg-slate-700 rounded-full w-1/2 animate-pulse"></div>
                </div>
            `;

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    mode: 'cors', 
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ 
                        prompt: `Create a professional 4-year career roadmap for a B.Tech ${branch} student specializing in ${interest}. List semesters, key skills, and 3 project ideas. Use bullet points.` 
                    })
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText || "Server Error");
                }

                const data = await response.json();

                if (data.roadmap) {
                    // Success View logic from the stable version
                    container.innerHTML = `
                        <div class="p-6 bg-slate-800/60 border border-slate-700 rounded-3xl shadow-2xl backdrop-blur-md">
                            <div class="text-slate-300 whitespace-pre-wrap font-medium">
                                ${data.roadmap.replace(/\*/g, '•')}
                            </div>
                        </div>
                        <div class="mt-4 bg-cyan-500/10 border border-cyan-500/20 p-4 rounded-2xl text-center">
                            <span class="text-cyan-400 text-[9px] font-black uppercase tracking-[0.2em]">Live from Gemini AI</span>
                        </div>
                    `;
                    window.scrollTo({ top: output.offsetTop - 20, behavior: 'smooth' });
                } else {
                    throw new Error("Empty roadmap data");
                }
            } catch (err) {
                console.error("Fetch Error:", err);
                container.innerHTML = `
                    <div class="p-6 bg-red-900/10 border border-red-500/20 rounded-3xl text-center">
                        <p class="text-red-400 text-xs font-bold mb-2 uppercase">Backend Connection Failed</p>
                        <p class="text-slate-500 text-[10px] mb-4">Error: ${err.message}</p>
                        <button onclick="location.reload()" class="px-4 py-2 bg-red-500/20 hover:bg-red-500/40 text-red-300 text-[10px] rounded-lg uppercase font-bold tracking-widest transition-colors">Retry Fix</button>
                    </div>
                `;
            } finally {
                btn.innerText = "GENERATE ROADMAP";
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>
