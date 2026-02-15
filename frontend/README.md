# 🎨 Draftly — Frontend

Next.js 16 web interface for the Draftly blog generator.

---

## 🚀 Setup

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Requires backend on `http://localhost:8000`.

---

## ✨ Features

- 📝 Topic input with platform selector and research toggle
- ⏳ Animated 5-step progress tracker
- 📖 Styled Markdown preview (headings, lists, code blocks)
- 📤 Copy · Download `.md` · Print as PDF
- 🔗 Clickable research source links

---

## 📁 Structure

```
├── app/
│   ├── page.tsx        # Main page (landing ↔ preview)
│   ├── layout.tsx      # Root layout
│   └── globals.css     # Styles + @media print
├── components/
│   ├── DraftForm.tsx   # Topic input + controls
│   ├── BlogPreview.tsx # Markdown renderer + export
│   ├── LoadingState.tsx # Progress animation
│   ├── SourcesSection.tsx
│   ├── Hero.tsx
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   └── ui/             # Shadcn primitives
└── lib/
    ├── api.ts          # Backend API client
    └── utils.ts        # Tailwind merge
```

## 🛠️ Tech

Next.js 16 · React 19 · Tailwind CSS v4 · Framer Motion · react-markdown · Shadcn UI · Sonner · Lucide
