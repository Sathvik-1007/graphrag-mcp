interface ThemeToggleProps {
  theme: "light" | "dark";
  onToggle: () => void;
}

export function ThemeToggle({ theme, onToggle }: ThemeToggleProps) {
  return (
    <button
      onClick={onToggle}
      className="px-3 py-1.5 rounded-md text-sm border border-[var(--color-border)] bg-[var(--color-bg)] hover:bg-[var(--color-border)] transition-colors cursor-pointer"
      title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
    >
      {theme === "dark" ? "☀ Light" : "● Dark"}
    </button>
  );
}
