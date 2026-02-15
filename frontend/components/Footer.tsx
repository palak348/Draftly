export function Footer() {
    return (
        <footer className="py-12 border-t border-white/5 bg-[#0b0b15] text-center">
            <div className="container mx-auto px-4">
                <p className="text-slate-600 text-sm">
                    Built with <span className="text-indigo-400">Next.js</span>, <span className="text-purple-400">FastAPI</span> & <span className="text-cyan-400">LangGraph</span>.
                </p>
                <p className="text-slate-700 text-xs mt-2">
                    © {new Date().getFullYear()} Draftly AI. All rights reserved.
                </p>
            </div>
        </footer>
    );
}
