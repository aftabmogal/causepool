import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const isAuthed = !!localStorage.getItem("access");

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/");
  };

  return (
    <header className="sticky top-0 z-30 bg-paper/90 backdrop-blur border-b border-ink/10">
      <nav className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        <Link to="/" className="font-display text-xl font-semibold tracking-tight text-ink">
          digital heroes
        </Link>
        <div className="flex items-center gap-7 text-sm font-medium text-inkmuted">
          <Link to="/charities" className="hover:text-ink transition-colors">Charities</Link>
          {isAuthed ? (
            <>
              <Link to="/dashboard" className="hover:text-ink transition-colors">Dashboard</Link>
              <button onClick={logout} className="hover:text-ink transition-colors">Sign out</button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-ink transition-colors">Sign in</Link>
              <Link
                to="/signup"
                className="bg-ink text-paper px-4 py-2 rounded-full hover:bg-coral transition-colors"
              >
                Join now
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
