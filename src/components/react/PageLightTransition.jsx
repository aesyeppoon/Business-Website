import { useEffect, useState } from "react";

export default function PageLightTransition() {
  const [active, setActive] = useState(false);

  useEffect(() => {
    let navigationTimer = 0;

    const runQuoteTransition = (event) => {
      const link = event.target.closest("a[data-quote-transition]");
      if (!link || window.sessionStorage.getItem("aes-quote-transition-used") === "1") {
        return;
      }

      event.preventDefault();
      window.sessionStorage.setItem("aes-quote-transition-used", "1");
      setActive(true);
      navigationTimer = window.setTimeout(() => {
        window.location.assign(link.href);
      }, 820);
    };

    document.addEventListener("click", runQuoteTransition);

    return () => {
      document.removeEventListener("click", runQuoteTransition);
      window.clearTimeout(navigationTimer);
    };
  }, []);

  return (
    <div
      className={`page-light-transition ${active ? "is-active" : ""}`}
      aria-hidden="true"
    >
      <span />
    </div>
  );
}
