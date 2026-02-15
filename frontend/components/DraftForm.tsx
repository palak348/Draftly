"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Globe, FileText, ChevronDown } from "lucide-react";
import { toast } from "sonner";
import { generateBlog } from "@/lib/api";
import { LoadingState } from "@/components/LoadingState";
import { Button } from "@/components/ui/button";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";


interface DraftFormProps {
    onSuccess: (data: any) => void;
}

export function DraftForm({ onSuccess }: DraftFormProps) {
    const [topic, setTopic] = useState("");
    const [platform, setPlatform] = useState("generic");
    const [loading, setLoading] = useState(false);
    const [researchEnabled, setResearchEnabled] = useState(true);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!topic.trim()) return;

        setLoading(true);
        try {
            const result = await generateBlog({
                topic,
                platform,
                enable_research: researchEnabled
            });
            onSuccess(result);
        } catch (error: any) {
            toast.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="w-full max-w-2xl mx-auto backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-12 text-center shadow-2xl animate-fade-in relative z-20">
                <LoadingState />
            </div>
        )
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="w-full max-w-2xl mx-auto relative z-20 px-4"
        >
            <form onSubmit={handleSubmit} className="relative group">
                {/* Glow behind container */}
                <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-cyan-500/20 rounded-3xl blur-2xl opacity-50 group-hover:opacity-75 transition duration-1000" />

                <div className="relative backdrop-blur-2xl bg-[#0f111a]/80 border border-white/10 rounded-2xl shadow-2xl overflow-hidden">

                    {/* Input Area */}
                    <div className="p-2">
                        <textarea
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="Describe the blog post you want to create..."
                            className="w-full bg-transparent border-none text-lg text-white placeholder:text-slate-500 outline-none p-4 min-h-[80px] resize-none"
                            rows={2}
                        />
                    </div>

                    {/* Controls Bar */}
                    <div className="bg-white/5 border-t border-white/5 p-3 flex flex-col md:flex-row items-center justify-between gap-4">

                        <div className="flex items-center gap-2 w-full md:w-auto overflow-x-auto pb-2 md:pb-0 scrollbar-hide">
                            <Select value={platform} onValueChange={setPlatform}>
                                <SelectTrigger className="w-[140px] bg-white/5 border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-colors h-9 rounded-lg focus:ring-0 focus:ring-offset-0">
                                    <SelectValue placeholder="Format" />
                                </SelectTrigger>
                                <SelectContent className="bg-[#1a1d2d] border-slate-700 text-slate-300">
                                    <SelectItem value="generic">Balanced</SelectItem>
                                    <SelectItem value="medium">Medium</SelectItem>
                                    <SelectItem value="devto">Dev.to</SelectItem>
                                    <SelectItem value="linkedin">LinkedIn</SelectItem>
                                </SelectContent>
                            </Select>

                            <div className="h-6 w-px bg-white/10 mx-2" />

                            <button
                                type="button"
                                onClick={() => setResearchEnabled(!researchEnabled)}
                                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${researchEnabled ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'text-slate-500 hover:text-slate-300'}`}
                            >
                                <Globe className="w-3.5 h-3.5" />
                                Research
                            </button>
                        </div>

                        <Button
                            type="submit"
                            disabled={!topic.trim()}
                            className="w-full md:w-auto h-10 px-6 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold transition-all hover:shadow-[0_0_20px_rgba(99,102,241,0.5)] border border-white/20"
                        >
                            <Sparkles className="w-4 h-4 mr-2" />
                            Generate Draft
                        </Button>
                    </div>
                </div>
            </form>
        </motion.div>
    );
}
