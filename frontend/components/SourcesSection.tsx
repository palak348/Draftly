export interface Source {
    title: string;
    url: string;
}

interface SourcesSectionProps {
    sources?: Source[];
}

export function SourcesSection({ sources }: SourcesSectionProps) {
    if (!sources || sources.length === 0) return null;

    return (
        <div className="mt-8 pt-8 border-t border-slate-300">
            <h3 className="text-lg font-bold mb-4 text-black">Sources</h3>
            <ul className="space-y-2 list-decimal list-inside text-sm text-slate-800">
                {sources.map((source, index) => (
                    <li key={index}>
                        <a
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:text-indigo-700 hover:underline transition-colors font-semibold text-slate-900"
                        >
                            {source.title || source.url}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
}
