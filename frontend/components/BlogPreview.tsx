"use client";

import Markdown from "react-markdown";
import { SourcesSection, type Source } from "@/components/SourcesSection";
import { Button } from "@/components/ui/button";
import { Download, RefreshCcw, FileText, Copy, ArrowUpRight } from "lucide-react";
import { toast } from "sonner";
import { useState } from "react";
import { motion } from "framer-motion";

interface BlogPreviewProps {
    content: string;
    title: string;
    sources?: Source[];
    onRegenerate: () => void;
}

export function BlogPreview({ content, title, sources, onRegenerate }: BlogPreviewProps) {
    const [isExporting, setIsExporting] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(content);
        toast.success("Markdown copied to clipboard");
    };

    const handleDownloadMd = () => {
        const blob = new Blob([content], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `draftly-${title.replace(/\s+/g, "-").toLowerCase()}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        toast.success("Markdown downloaded");
    };

    const handleDownloadPdf = () => {
        window.print();
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="relative w-full max-w-4xl mx-auto"
        >
            {/* Background Glow */}
            <div data-html2canvas-ignore="true" className="absolute top-0 inset-x-0 h-40 bg-gradient-to-b from-indigo-500/10 to-transparent blur-3xl pointer-events-none" />

            <div id="blog-export-container" className="relative border border-slate-200 rounded-2xl bg-white shadow-xl overflow-hidden text-slate-900">

                {/* Header/Title Bar */}
                <div className="border-b border-slate-100 bg-slate-50/50 p-6 md:p-10 text-center">
                    <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-slate-900 mb-4">
                        {title}
                    </h1>
                </div>

                <div id="blog-content" className="p-8 md:p-12 prose prose-lg max-w-none prose-headings:text-black prose-p:text-slate-900 prose-strong:text-black prose-ul:text-slate-900">
                    <Markdown
                        components={{
                            h1: ({ node, ...props }) => <h1 className="hidden" {...props} />, // Title is already shown above
                            h2: ({ node, ...props }) => (
                                <h2 className="text-2xl font-bold text-black mt-12 mb-6 flex items-center gap-3 group" {...props}>
                                    <span className="w-1.5 h-8 bg-indigo-600 rounded-full" />
                                    {props.children}
                                </h2>
                            ),
                            h3: ({ node, ...props }) => <h3 className="text-xl font-bold text-slate-900 mt-8 mb-4 border-l-4 border-indigo-500 pl-4" {...props} />,
                            p: ({ node, ...props }) => <p className="text-slate-900 leading-relaxed mb-6 font-medium" {...props} />,
                            strong: ({ node, ...props }) => <strong className="font-bold text-black" {...props} />,
                            ul: ({ node, ...props }) => <ul className="my-6 space-y-2 list-none" {...props} />,
                            li: ({ node, ...props }) => (
                                <li className="flex gap-3 text-slate-900 font-medium">
                                    <div className="mt-2 w-1.5 h-1.5 rounded-full bg-indigo-500 shrink-0" />
                                    <span>{props.children}</span>
                                </li>
                            ),
                            blockquote: ({ node, ...props }) => (
                                <blockquote className="my-8 pl-6 border-l-4 border-indigo-500 italic text-slate-800 bg-slate-50 p-4 rounded-r-lg" {...props} />
                            ),
                            img: ({ node, ...props }) => null, // Suppress any residual images
                            a: ({ node, ...props }) => (
                                <a
                                    className="text-indigo-700 hover:text-indigo-800 hover:underline cursor-pointer transition-colors font-semibold"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    {...props}
                                />
                            ),
                            code: ({ node, ...props }) => (
                                <code className="bg-slate-100 text-indigo-700 px-1.5 py-0.5 rounded text-sm font-mono border border-slate-300" {...props} />
                            ),
                        }}
                    >
                        {content}
                    </Markdown>

                    <SourcesSection sources={sources} />
                </div>
            </div>

            {/* Floating Action Bar */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1, duration: 0.5 }}
                className="sticky bottom-8 z-20 flex justify-center w-full"
            >
                <div className="flex items-center gap-2 p-2 rounded-full bg-[#0b0b15]/80 backdrop-blur-xl border border-white/10 shadow-2xl shadow-black/50">
                    <Button variant="ghost" size="sm" onClick={handleCopy} className="text-slate-400 hover:text-white hover:bg-white/10 rounded-full px-4">
                        <Copy className="mr-2 h-3.5 w-3.5" />
                        Copy
                    </Button>
                    <div className="w-px h-4 bg-white/10" />
                    <Button variant="ghost" size="sm" onClick={handleDownloadMd} className="text-slate-400 hover:text-white hover:bg-white/10 rounded-full px-4">
                        <FileText className="mr-2 h-3.5 w-3.5" />
                        MD
                    </Button>
                    <div className="w-px h-4 bg-white/10" />
                    <Button
                        size="sm"
                        onClick={handleDownloadPdf}
                        disabled={isExporting}
                        className="bg-indigo-600 hover:bg-indigo-500 text-white rounded-full px-6 shadow-lg shadow-indigo-500/20"
                    >
                        {isExporting ? <RefreshCcw className="mr-2 h-3.5 w-3.5 animate-spin" /> : <Download className="mr-2 h-3.5 w-3.5" />}
                        Download PDF
                    </Button>
                    <Button variant="ghost" size="icon" onClick={onRegenerate} className="rounded-full text-slate-400 hover:text-white hover:bg-white/10 ml-1">
                        <RefreshCcw className="h-4 w-4" />
                    </Button>
                </div>
            </motion.div>
        </motion.div>
    );
}
