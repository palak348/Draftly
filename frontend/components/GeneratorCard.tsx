"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateBlog } from "@/lib/api";
import { LoadingState } from "@/components/LoadingState";
import { BlogPreview } from "@/components/BlogPreview";
import { toast } from "sonner";
import { Settings2, Sparkles } from "lucide-react";

export function GeneratorCard() {
    const [topic, setTopic] = useState("");
    const [platform, setPlatform] = useState("generic");
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!topic.trim()) {
            toast.error("Please enter a topic");
            return;
        }

        setIsLoading(true);
        setResult(null);

        try {
            const data = await generateBlog({
                topic,
                platform,
                enable_research: true, // Hardcoded for now based on UI request, could be toggles
                enable_images: true
            });
            setResult(data);
            toast.success("Blog generated successfully!");
        } catch (error: any) {
            toast.error(error.message || "Something went wrong");
        } finally {
            setIsLoading(false);
        }
    };

    if (result) {
        return (
            <BlogPreview
                content={result.content}
                title={result.title}
                sources={result.metadata?.sources}
                onRegenerate={() => setResult(null)}
            />
        );
    }

    return (
        <Card className="w-full max-w-2xl mx-auto border shadow-lg bg-card/50 backdrop-blur-sm">
            <CardHeader>
                <CardTitle className="text-2xl font-bold text-center flex items-center justify-center gap-2">
                    <Sparkles className="h-6 w-6 text-primary" />
                    Create New Draft
                </CardTitle>
                <CardDescription className="text-center text-base">
                    Enter your topic and let AI research, plan, and write for you.
                </CardDescription>
            </CardHeader>
            <CardContent>
                {isLoading ? (
                    <LoadingState />
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <Label htmlFor="topic">What do you want to write about?</Label>
                            <Textarea
                                id="topic"
                                placeholder="e.g. The future of quantum computing in finance..."
                                className="min-h-[100px] text-lg resize-none"
                                value={topic}
                                onChange={(e) => setTopic(e.target.value)}
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="platform">Platform Tone</Label>
                                <Select value={platform} onValueChange={setPlatform}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select platform" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="generic">Generic (Balanced)</SelectItem>
                                        <SelectItem value="medium">Medium (Detailed)</SelectItem>
                                        <SelectItem value="devto">Dev.to (Technical)</SelectItem>
                                        <SelectItem value="linkedin">LinkedIn (Professional)</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="flex items-end pb-2">
                                <div className="flex items-center gap-2 text-sm text-muted-foreground bg-muted/50 p-2 rounded-md w-full justify-center">
                                    <Settings2 className="h-4 w-4" />
                                    <span>Auto-Research & Images Enabled</span>
                                </div>
                            </div>
                        </div>

                        <Button type="submit" className="w-full text-lg h-12 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 transition-all font-semibold shadow-lg shadow-indigo-500/20">
                            Generate Blog
                        </Button>
                    </form>
                )}
            </CardContent>
        </Card>
    );
}
