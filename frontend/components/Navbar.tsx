"use client";

import Link from "next/link";
import { Github } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Navbar() {
    return (
        <nav className="fixed top-0 z-50 w-full border-b border-white/5 bg-[#0b0b15]/80 backdrop-blur-xl transition-all duration-300">
            <div className="container flex h-16 items-center justify-between mx-auto px-6">

                {/* Logo Area */}
                <Link href="/" className="flex items-center gap-2 group">
                    <div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/10 border border-indigo-500/20 group-hover:border-indigo-500/40 transition-colors">
                        <div className="w-4 h-4 rounded-sm bg-indigo-500 rotate-45 group-hover:rotate-90 transition-transform duration-500" />
                    </div>
                    <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent group-hover:to-white transition-all">
                        Draftly
                    </span>
                </Link>

                {/* Actions */}
                <div className="flex items-center gap-4">
                    <Link
                        href="https://github.com/your-username/draftly"
                        target="_blank"
                        rel="noreferrer"
                        className="text-slate-400 hover:text-white transition-colors"
                    >
                        <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/5 transition-all text-sm font-medium">
                            <Github className="h-4 w-4" />
                            <span>Star on GitHub</span>
                        </div>
                    </Link>
                </div>
            </div>
        </nav>
    );
}
