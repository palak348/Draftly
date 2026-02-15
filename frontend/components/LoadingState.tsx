"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, Circle, Sparkles, BrainCircuit, PenTool, LayoutTemplate } from "lucide-react";

const LOADING_STEPS = [
    { text: "Analyzing topic & intent...", icon: BrainCircuit, duration: 2500 },
    { text: "Deep web research...", icon: Sparkles, duration: 4000 },
    { text: "Synthesizing insights...", icon: LayoutTemplate, duration: 3000 },
    { text: "Drafting content & sections...", icon: PenTool, duration: 3000 },
    { text: "Final polish & formatting...", icon: CheckCircle2, duration: 2000 },
];

export function LoadingState() {
    const [currentStep, setCurrentStep] = useState(0);

    useEffect(() => {
        let totalDelay = 0;

        LOADING_STEPS.forEach((step, index) => {
            if (index === 0) return;
            totalDelay += LOADING_STEPS[index - 1].duration;
            setTimeout(() => {
                setCurrentStep(index);
            }, totalDelay);
        });
    }, []);

    return (
        <div className="w-full max-w-md mx-auto p-8 rounded-2xl bg-[#0f111a]/50 backdrop-blur-xl border border-white/10 shadow-2xl relative overflow-hidden">
            {/* Background Glow */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-64 bg-indigo-500/20 blur-[80px] rounded-full pointer-events-none" />

            <div className="relative z-10 flex flex-col items-center gap-6">

                {/* Main Icon */}
                <div className="relative">
                    <div className="absolute inset-0 bg-indigo-500/30 blur-xl rounded-full animate-pulse" />
                    <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                        <Sparkles className="w-8 h-8 text-white animate-pulse" />
                    </div>
                </div>

                {/* Progress Text */}
                <div className="text-center space-y-2">
                    <h3 className="text-xl font-semibold text-white tracking-tight">
                        Creating Masterpiece
                    </h3>
                    <p className="text-slate-400 text-sm">
                        Researching and writing your research-grade article.
                    </p>
                </div>

                {/* Steps List */}
                <div className="w-full space-y-3 mt-4">
                    {LOADING_STEPS.map((step, index) => {
                        const Icon = step.icon;
                        const status =
                            index < currentStep ? "completed"
                                : index === currentStep ? "active"
                                    : "waiting";

                        return (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className={`flex items-center gap-3 p-3 rounded-xl transition-all duration-500 ${status === "active" ? "bg-white/5 border border-white/10 shadow-lg"
                                    : "opacity-50"
                                    }`}
                            >
                                <div className={`relative flex items-center justify-center w-6 h-6 rounded-full transition-colors ${status === "completed" ? "bg-emerald-500/20 text-emerald-400"
                                    : status === "active" ? "bg-indigo-500/20 text-indigo-400 animate-pulse"
                                        : "bg-white/5 text-slate-500"
                                    }`}>
                                    {status === "completed" ? (
                                        <CheckCircle2 className="w-4 h-4" />
                                    ) : (
                                        <Icon className="w-3.5 h-3.5" />
                                    )}
                                </div>

                                <span className={`text-sm font-medium ${status === "active" ? "text-white"
                                    : status === "completed" ? "text-slate-300 line-through decoration-slate-600"
                                        : "text-slate-500"
                                    }`}>
                                    {step.text}
                                </span>

                                {status === "active" && (
                                    <div className="ml-auto flex gap-1">
                                        <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1 }} className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                                        <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                                        <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                                    </div>
                                )}
                            </motion.div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
