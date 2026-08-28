export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <div className="mb-8">
        <span className="text-6xl">🚀</span>
      </div>
      <h1 className="text-4xl font-bold text-foreground mb-4">
        Workshop PopiAI — Ready
      </h1>
      <p className="text-lg text-body mb-8 max-w-md">
        El proyecto base está configurado correctamente. Durante el workshop
        implementaremos features usando Claude Code.
      </p>
      <div className="flex flex-col gap-3 w-full max-w-sm">
        <a
          href="http://localhost:3001/api/health"
          target="_blank"
          rel="noreferrer"
          className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary-hover transition-colors font-medium text-center"
        >
          Verificar Backend →
        </a>
        <div className="text-sm text-body">
          <p>Backend: http://localhost:3001/api</p>
          <p>Frontend: http://localhost:3000</p>
        </div>
      </div>
    </div>
  );
}
