"use client";

import { useState } from "react";
import { Hero } from "@/components/Hero";
import { DraftForm } from "@/components/DraftForm";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { BlogPreview } from "@/components/BlogPreview";
import { AnimatePresence, motion } from "framer-motion";

export default function Home() {
  const [result, setResult] = useState<any>(null);

  return (
    <main className="min-h-screen bg-[#0b0b15] text-white selection:bg-indigo-500/30 font-sans">
      <Navbar />

      <AnimatePresence mode="wait">
        {!result ? (
          <motion.div
            key="landing"
            exit={{ opacity: 0, y: -20 }}
            className="flex flex-col min-h-screen"
          >
            <div className="flex-1">
              <div className="relative">
                <Hero />
                <div className="-mt-16 mb-20 relative z-30 px-4">
                  <DraftForm onSuccess={setResult} />
                </div>
              </div>

            </div>

            <Footer />
          </motion.div>
        ) : (
          <motion.div
            key="result"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="container mx-auto px-4 py-12 max-w-4xl"
          >
            <div className="mb-8">
              <button
                onClick={() => setResult(null)}
                className="text-slate-400 hover:text-white flex items-center gap-2 text-sm transition-colors group"
              >
                <span className="group-hover:-translate-x-1 transition-transform">←</span> Back to Generator
              </button>
            </div>
            <BlogPreview
              content={result.content}
              title={result.title}
              sources={result.metadata?.sources}
              onRegenerate={() => setResult(null)}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
