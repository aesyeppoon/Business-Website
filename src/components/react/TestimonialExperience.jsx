const experiences = [
  {
    title: "Easy to deal with",
    text:
      "Communication was clear from the start, everything was explained properly and the job was completed exactly as discussed.",
    context: "Homeowner | Yeppoon",
  },
  {
    title: "Left everything neat",
    text:
      "The work was completed carefully and the area was left clean and tidy. It was a very straightforward experience.",
    context: "Residential customer | Rockhampton",
  },
  {
    title: "Found the fault quickly",
    text:
      "The problem was properly tested, clearly explained and repaired without any unnecessary fuss or guesswork.",
    context: "Property maintenance | Central Queensland",
  },
  {
    title: "Minimal disruption",
    text:
      "The electrical work was organised around our operating hours and completed with very little interruption to the business.",
    context: "Commercial customer | Central Queensland",
  },
  {
    title: "Practical advice",
    text:
      "We were given sensible options that suited the house and our budget, with no pressure to add work we did not need.",
    context: "Renovation customer | Yeppoon",
  },
];

function TestimonialCard({ experience, index }) {
  return (
    <article className="testimonial-marquee__card">
      <span className="testimonial-marquee__number">0{index + 1}</span>
      <span className="testimonial-marquee__quote" aria-hidden="true">“</span>
      <h2>{experience.title}</h2>
      <p>{experience.text}</p>
      <strong>{experience.context}</strong>
    </article>
  );
}

export default function TestimonialExperience() {
  const loop = [...experiences, ...experiences];

  return (
    <div className="testimonial-experience">
      <div className="testimonial-experience__flare" aria-hidden="true" />
      <div className="testimonial-experience__lines" aria-hidden="true" />

      <section className="testimonial-marquee">
        <div className="container testimonial-marquee__intro">
          <span className="eyebrow">Testimonials</span>
          <h2>What customers value about working with us.</h2>
          <p>
            Clear communication, practical advice and electrical work completed
            carefully across homes, rentals and local businesses.
          </p>
        </div>

        <div className="testimonial-marquee__viewport" aria-label="Service experience highlights">
          <div className="testimonial-marquee__track">
            {loop.map((experience, index) => (
              <TestimonialCard
                experience={experience}
                index={index % experiences.length}
                key={`${experience.title}-${index}`}
              />
            ))}
          </div>
        </div>

        <div className="testimonial-marquee__rail" aria-hidden="true">
          <span />
        </div>
      </section>

    </div>
  );
}
