"""Narration script for the JSP-000005 exposition video.

Each slide is a list of sentences. A sentence is either a string (used for both
speech and subtitle) or a (subtitle, spoken) pair when pronunciation differs.
"""

SLIDES = [
    # 1 title
    [
        "This video is a companion to the essay, How a Forced Navier–Stokes Flow Blows Up.",
        "It explains, step by step, the finite-time blowup construction that OpenAI released in September 2026 for the three-dimensional Navier–Stokes equations.",
        "All of the mathematics is due to the authors of that paper. This is an exposition.",
    ],
    # 2 question
    [
        "The Navier–Stokes equations describe a viscous, incompressible fluid.",
        "The velocity u changes because of transport by the flow itself, viscosity, the pressure gradient, and an external force f.",
        "Fefferman's official Clay problem statement offers four alternatives.",
        "A and B ask for global smooth solutions without any force, on the whole space or on the torus.",
        "C and D ask instead for a breakdown: smooth, rapidly decaying data and force for which no smooth solution with bounded energy exists for all time.",
        "The important detail is that C and D allow a force.",
    ],
    # 3 result
    [
        "Here is the theorem.",
        "For every positive viscosity, there is a smooth force, compactly supported in space and time, and a flow that starts from rest.",
        "Its velocity and pressure stay inside a fixed compact set, its energy stays bounded, and its maximum speed becomes infinite at time one.",
        "So no global smooth solution with bounded energy exists for that force. This is alternative C.",
        "A rescaling and periodization argument then gives alternative D on the torus.",
        "Two caveats matter. The unforced questions, A and B, are untouched.",
        "And as of this recording, the result has not been independently peer reviewed, although a Lean formalization has been released.",
    ],
    # 4 why hard
    [
        "Why are three dimensions hard?",
        "The equations have a scaling symmetry: zooming in by a factor lambda maps solutions to solutions.",
        "Under this scaling the energy shrinks by a factor of lambda.",
        "Zooming into small scales therefore weakens the only global bound we have, so energy alone cannot rule out concentration.",
        ("Leray built global weak solutions in 1934, and Caffarelli, Kohn and Nirenberg showed that the singular set must be small.",
         "Leray built global weak solutions in 1934, and Caffarelli, Kohn and Nirenberg showed that the singular set must be small."),
        "Tao showed that an averaged version of the equations can blow up.",
        ("Córdoba, Martínez-Zoroa and coauthors built forced singularities for Euler and for hypodissipative models.",
         "Cordoba, Martinez-Zoroa and coauthors built forced singularities for Euler and for hypodissipative models."),
        "The new work follows this forced line, but at full viscosity, and with a smooth force.",
    ],
    # 5 reformulation
    [
        "The first idea is almost a tautology.",
        "Take any smooth, incompressible velocity and pressure, and compute the momentum residual: the time derivative, plus transport, minus viscosity, plus the pressure gradient.",
        "Call the result f. Then the pair solves Navier–Stokes with force f. Every flow is a forced flow.",
        "So the whole difficulty moves into one question.",
        "Can we design a flow that blows up, while its residual, and every derivative of it, extends smoothly through the singular time?",
        "Each term in the residual blows up on its own, so they must cancel to infinite order.",
        "The paper states this as a flatness estimate: every derivative of the residual is smaller than every power of q, a scale that measures the distance to the singular point.",
    ],
    # 6 vortex
    [
        "Here is the flow. Use cylindrical coordinates around a vertical axis, and let tau be the time remaining.",
        "In a central core, fluid spirals inward and leaves along the axis, upward and downward.",
        "Inflow conserves angular momentum, so the fluid spins faster. Viscosity carries angular momentum back out, and the speed grows as the balance between the two.",
        "Around the core sits an annulus, where oscillating pulses will live.",
        "Outside is a purely rotating exterior that solves the heat equation for the swirl exactly, so it needs no force at all.",
        "The core is anisotropic. Its radius shrinks like tau to the one half, while its height shrinks more slowly, like tau to the one half minus h, where h is a fixed number below one hundredth.",
        "So the core becomes an ever thinner column.",
    ],
    # 7 scales
    [
        "The speeds grow like tau to the minus one half minus h.",
        "Multiply by the core volume, and the kinetic energy scales like tau to the one half minus three h, which goes to zero.",
        "The dissipation rate scales like tau to the minus one half minus three h, which is integrable in time because h is less than one sixth.",
        "So the blowup is invisible to the energy.",
        "But the critical quantity, the square root of tau times the maximum speed, grows like tau to the minus h.",
        "The swirl Reynolds number diverges, while the radial Reynolds number stays bounded, so viscosity remains in the leading balance.",
    ],
    # 8 annular stress
    [
        "The core balances its own momentum, and so does the heat exterior. The trouble is where they meet.",
        "In the annulus, the background leaves a residual that becomes unbounded at time one, so it cannot serve as the force.",
        "The paper writes that residual as the radial divergence of a stress T, with two components: the radial flux of swirl momentum, and the radial flux of axial momentum.",
        "The annulus does not need momentum injected. It needs momentum moved radially, and a stress is exactly a momentum flux.",
        "The profiles are tuned, by matching five radial integrals and by adding a small logarithmic oscillation, so that this stress vanishes outside the annulus and has the right shape for the next step.",
    ],
    # 9 pulses
    [
        "Now the key mechanism. Add an oscillating velocity w on top of the background.",
        "The residual picks up a linear term, and a quadratic term: the divergence of w tensor w. That is a Reynolds stress.",
        "Take a single plane wave: a cosine, with amplitude a perpendicular to its wave vector.",
        "It is exactly incompressible, it does not interact with itself, and its average stress is one half of a tensor a.",
        "With a slowly varying amplitude, the averaged stress becomes a force we can prescribe.",
        "Each family of waves contributes one fixed direction, weighted by a squared, and therefore positive, amplitude.",
        "With two families, any target inside the cone they span can be produced. That is the admissible stress cone condition, and the profiles were built to satisfy it.",
    ],
    # 10 amplification
    [
        "Where do the pulses get their energy? From the background shear.",
        "A toy model shows the centrifugal part. A parcel carrying extra swirl is flung outward.",
        "If angular momentum decreases outward, the parcel lands among slower fluid, and its surplus grows. This is Rayleigh's criterion.",
        "Each pulse is seeded by an exponentially small force, and then amplified.",
        "Differential rotation tilts the wave fronts, so the radial wavenumber grows. Amplification weakens while viscous damping strengthens.",
        "So each pulse rises and then decays within a short window.",
        "Pulses are placed on finer and finer scales as time approaches one, and an auxiliary torus variable keeps distinct pulses from interacting.",
    ],
    # 11 correction cycle
    [
        "The pulses cancel the leading stress, but they leave errors: linear terms, harmonics, mean flows, and curl and cutoff terms.",
        "The paper runs a correction cycle with four operations.",
        "It solves the wave amplitude equations, adjusts the amplitudes to fix the averaged stress, corrects the mean flow, and restores the radial moments.",
        "After every operation, the full residual is recomputed.",
        "Each cycle improves the decay exponent sigma by one tenth, starting from one fifth.",
        "The infinitely many corrections are then summed, with cutoffs whose supports shrink toward the singular point.",
        "The result is a flow whose residual is flat: smaller than every power of q, together with all of its derivatives.",
    ],
    # 12 finishing
    [
        "Five steps finish the proof.",
        "First, multiply the vector potential and the pressure by a cutoff, and take the curl afterwards, so the flow stays incompressible and compactly supported.",
        "Second, every derivative of the force has a limit at time one, so a Borel-type lemma extends the force smoothly beyond it.",
        "Third, pairing the equation with u bounds the energy by the square of the integrated force.",
        "Fourth, a uniqueness argument, which controls the pressure through Riesz transforms, shows that any smooth bounded-energy solution with the same data coincides with this flow before time one, so it must blow up as well.",
        "Fifth, rescaling handles every viscosity, and periodizing a shrunken copy gives the torus case.",
    ],
    # 13 Lean
    [
        "The Lean formalization states alternatives C and D in Lean 4, adapting Google DeepMind's Formal Conjectures statement of Fefferman's problem.",
        "The challenge file defines the decay conditions, smoothness, the equation, incompressibility and bounded energy, and leaves the two theorems unproved.",
        "The repository proves them, and the Comparator configuration permits only the three standard axioms: propositional extensionality, quotient soundness, and classical choice.",
        "What does this certify? That the stated theorems follow from Lean and Mathlib.",
        "Whether the formal statement faithfully matches the Clay text is a human question, and the definitions are short enough to check by reading.",
        "We did not rebuild the project ourselves.",
    ],
    # 14 summary
    [
        "To summarize.",
        "Collapse an anisotropic vortex. Let amplified pulses supply its missing momentum flux through their Reynolds stress.",
        "Correct to infinite order, so that the leftover force is smooth through the singular time. Then localize, extend the force, and prove uniqueness.",
        "The unforced problems, A and B, remain open, and independent review of the 166-page argument is still pending.",
        "The essay, with section references, scale checks, and a reading map, is linked in the description. Thank you for watching.",
    ],
]
