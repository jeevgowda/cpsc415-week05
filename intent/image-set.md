# Intent: An image set for product listings, with the critique checked

## Purpose
Team Project 1 (the product listing image generator) turns a seller's brief into product photos for an
online listing. For this lab I generate five listing photos of one product from one prompt family, have a
vision model check each photo against a yes/no checklist made from its prompt's requirements, and check
those answers in code. The photos are what a buyer sees, so a wrong photo (wrong color, extra objects,
misspelled text on the product) costs a seller a sale.

## The prompt family
One product, a white ceramic coffee mug with the word "MORNING" printed on it in black capital letters,
shown five ways: front view, top-down view, handle close-up, three-quarter angle, and a lifestyle shot on a
wooden table. Only the view changes; the product, the printed word, the plain style, and "no people, no
logos, no other text" stay fixed. Each prompt has a fixed seed so the set can be regenerated.

## What must not go wrong
1. **Trusting the critic.** The critique is model output and may be wrong in either direction: it can say a
   requirement is unmet when it is met, or met when it is not, and it can misread printed text. The program
   must make that visible, never hide it.
2. **Text on the product.** Image models misspell text and critics misread it. The expected word is compared
   in code with what the model reads back, letter for letter (ignoring case and punctuation).
3. **A critique that is not the checklist.** A reply that is not JSON, that skips a requirement, or that adds
   requirements nobody asked for is a problem the code reports, not a crash and not a pass.
4. **Cost.** One generation per prompt and one critique per image. No model call inside a test loop.

## How I will know the critic is wrong
- A second vision model answers the same checklist, and the code lists every disagreement.
- I look at every image myself before reading the critiques, and I read the printed word letter by letter.
- I ask one model an open-ended "what is wrong with this photo?" and check its claims against my eyes.

## Out of scope
Serving the images in the app (that is Team Project 1's code), and hosting.

## Approved by
Jeevan Gowda Kumaraswamy, November 2, 2026
