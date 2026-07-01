import { useEffect, useRef, useState } from "react";

export default function HeroLightController() {
  const controllerRef = useRef(null);
  const [progress, setProgress] = useState(0);
  const [complete, setComplete] = useState(false);
  const completeRef = useRef(false);

  useEffect(() => {
    const alreadyComplete =
      window.sessionStorage.getItem("aes-hero-light-complete") === "1";

    if (alreadyComplete) {
      document.documentElement.classList.add("aes-hero-light-complete");
      completeRef.current = true;
      setProgress(1);
      setComplete(true);
      return undefined;
    }

    let frame = 0;

    const update = () => {
      if (completeRef.current) return;

      const stage = controllerRef.current?.closest(".hero-stage");
      if (!stage) return;

      const header = document.querySelector(".site-header");
      const headerHeight = header?.getBoundingClientRect().height ?? 0;
      const rect = stage.getBoundingClientRect();
      const distance = Math.max(stage.offsetHeight - (window.innerHeight - headerHeight), 1);
      const next = Math.min(Math.max((headerHeight - rect.top) / distance, 0), 1);

      if (next >= 0.7) {
        completeRef.current = true;
        window.sessionStorage.setItem("aes-hero-light-complete", "1");
        const settleHero = () => {
          document.documentElement.scrollTop = 0;
          document.body.scrollTop = 0;
        };
        const blockMomentum = (event) => event.preventDefault();
        const blockScrollKeys = (event) => {
          if (["ArrowDown", "ArrowUp", "PageDown", "PageUp", " ", "Home", "End"].includes(event.key)) {
            event.preventDefault();
          }
        };
        window.addEventListener("wheel", blockMomentum, { passive: false });
        window.addEventListener("touchmove", blockMomentum, { passive: false });
        window.addEventListener("keydown", blockScrollKeys, { passive: false });

        let lastScrollY = window.scrollY;
        let quietFrames = 0;
        let settleFrame = 0;

        const collapseStage = () => {
          const previousHtmlAnchor = document.documentElement.style.overflowAnchor;
          const previousBodyAnchor = document.body.style.overflowAnchor;
          const previousScrollBehavior =
            document.documentElement.style.getPropertyValue("scroll-behavior");
          const previousScrollPriority =
            document.documentElement.style.getPropertyPriority("scroll-behavior");
          document.documentElement.style.overflowAnchor = "none";
          document.body.style.overflowAnchor = "none";
          document.documentElement.style.setProperty("scroll-behavior", "auto", "important");
          settleHero();
          document.documentElement.classList.add("aes-hero-light-complete");
          settleHero();
          requestAnimationFrame(() => {
            settleHero();
            requestAnimationFrame(() => {
              settleHero();
              document.documentElement.style.overflowAnchor = previousHtmlAnchor;
              document.body.style.overflowAnchor = previousBodyAnchor;
              if (previousScrollBehavior) {
                document.documentElement.style.setProperty(
                  "scroll-behavior",
                  previousScrollBehavior,
                  previousScrollPriority,
                );
              } else {
                document.documentElement.style.removeProperty("scroll-behavior");
              }
              window.removeEventListener("wheel", blockMomentum);
              window.removeEventListener("touchmove", blockMomentum);
              window.removeEventListener("keydown", blockScrollKeys);
            });
          });
        };

        const waitForMomentum = () => {
          const currentScrollY = window.scrollY;
          if (Math.abs(currentScrollY - lastScrollY) < 0.5) {
            quietFrames += 1;
          } else {
            quietFrames = 0;
            lastScrollY = currentScrollY;
          }

          if (quietFrames >= 18) {
            collapseStage();
            return;
          }

          settleFrame = requestAnimationFrame(waitForMomentum);
        };

        settleFrame = requestAnimationFrame(waitForMomentum);
        setProgress(1);
        setComplete(true);
        return;
      }

      setProgress(next / 0.7);
    };

    const onScroll = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(update);
    };

    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, []);

  const light = Math.min(progress / 0.72, 1);
  const release = Math.max((progress - 0.7) / 0.3, 0);

  return (
    <div
      ref={controllerRef}
      className={`hero-light ${complete ? "is-complete" : ""}`}
      style={{
        "--hero-light": light,
        "--hero-release": release,
      }}
      aria-hidden="true"
    >
      <div className="hero-light__darkness" />
      <div className="hero-light__glow" />
      <div className="hero-light__bulb">
        <div className="hero-light__rays">
          {Array.from({ length: 8 }, (_, index) => (
            <span key={index} style={{ "--ray": index }} />
          ))}
        </div>
        <img
          src="/images/aes-bulb-mirrored.png"
          alt=""
        />
      </div>
      <div className="hero-light__prompt">
        <span>Adaptive Electrical Solutions</span>
        <strong>Scroll to bring the power on</strong>
      </div>
      <div className="hero-light__meter"><span /></div>
    </div>
  );
}
