export interface GenerateRequest {
    topic: string;
    platform: string;
    enable_research?: boolean;
}

export interface GenerateResponse {
    title: string;
    content: string;
    word_count: number;
    sections: number;
    platform: string;
    topic: string;
    metadata?: any;
}

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function generateBlog(data: GenerateRequest): Promise<GenerateResponse> {
    const response = await fetch(`${BACKEND_URL}/generate-blog`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            topic: data.topic,
            platform: data.platform,
            enable_research: data.enable_research,
        }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(errorData.detail || "Failed to generate blog");
    }

    return response.json();
}

