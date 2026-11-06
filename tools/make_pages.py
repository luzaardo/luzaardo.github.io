#!/usr/bin/env python3
"""One-time generator for the two case-study page templates.
After the pages exist, content changes go through the page editor + tools/apply_editor_export.py
(this script would overwrite them, so do not re-run it)."""
import sys
R = '/home/claude/luzaardo.github.io/'
n_img = [0]

def slot(ratio='4/3', label=None):
    n_img[0] += 1
    return f'<div class="img-slot" data-ratio="{ratio}" data-label="Image {n_img[0]} placeholder ({ratio.replace("/", ":")})"></div>'

def fig(ratio, cap):
    return f'<figure>{slot(ratio)}<figcaption>{cap}</figcaption></figure>'

def figs(kind, ratio, caps):
    return f'<div class="figs {kind}">' + ''.join(fig(ratio, c) for c in caps) + '</div>'

def ul(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def page(title, tag1, tag2, subtitle, platform, timeline, team, other_href):
    n_img[0] = 0
    hero = f'''<section class="hero">
      {slot('21/9')}
      <div class="hero-inner">
        <ul class="tags" aria-label="Project keywords"><li>{tag1}</li><li>{tag2}</li></ul>
        <h1>{title}</h1>
        <p class="hero-sub">{subtitle}</p>
        <div class="meta">
          <div><span class="t">Platform</span><span class="v">{platform}</span></div>
          <div><span class="t">Timeline</span><span class="v">{timeline}</span></div>
          <div><span class="t">Team</span><span class="v">{team}</span></div>
        </div>
      </div>
    </section>'''
    glance = '''<section>
      <p class="eyebrow">At a glance</p>
      <h2>Headline: one sentence that states what you did and the result it created.</h2>
      <p>Overview, paragraph 1: Introduce the project in two or three sentences. Who was it for, and what problem was it meant to solve?</p>
      <p>Overview, paragraph 2: Describe the size of the work and your part in it. How long did it run, who was on the team, and what did you own?</p>
    </section>'''
    role = '''<section>
      <h3 class="label">Role and responsibilities</h3>
      <p>Role summary: Your title on this project and the one sentence that says what you were responsible for.</p>
      <ol>
        <li>Responsibility 1: A key action you took, starting with a verb (for example, "Led usability testing with…").</li>
        <li>Responsibility 2: Another key action and the method you used.</li>
        <li>Responsibility 3: Another key action and who you worked with.</li>
        <li>Responsibility 4: Another key action and what it produced.</li>
        <li>Responsibility 5: Another key action and how you checked it worked.</li>
      </ol>
    </section>'''
    metric = lambda k: f'<div class="metric"><div class="num">Result {k}</div><div class="desc">What this number measures, and the period it covers.</div></div>'
    results = f'''<section>
      <h3 class="label">Key results</h3>
      <div class="metrics">{''.join(metric(k) for k in range(1, 5))}</div>
    </section>'''
    note = '''<section>
      <div class="note"><p>Confidentiality note (optional): Say what was changed or left out to protect private information, and whose views this case study reflects.</p></div>
    </section>'''
    problem = f'''<section>
      <p class="eyebrow">The problem</p>
      <h2>Problem headline: the situation or user need that made this project necessary.</h2>
      <p>Problem, paragraph 1: Explain the context. Who are the users, and what was not working for them?</p>
      <p>Problem, paragraph 2: Explain why it mattered, using a number or a quote if you have one.</p>
      <h3 class="label center">These challenges meant:</h3>
      {figs('three', '3/4', ['Challenge 1: What users or staff struggled with, in one line.', 'Challenge 2: What users or staff struggled with, in one line.', 'Challenge 3: What users or staff struggled with, in one line.'])}
    </section>'''
    goal = lambda k: f'<div class="goal"><h3>Goal {k}</h3><p>Goal {k} description: What you set out to improve, in one sentence.</p></div>'
    goals = f'''<section>
      <h3 class="label center">Our team set 3 core goals:</h3>
      <div class="goals">{''.join(goal(k) for k in range(1, 4))}</div>
    </section>'''
    discovery = f'''<section>
      <p class="eyebrow">Discovery</p>
      <h2>Research headline: what you learned, and how you learned it.</h2>
      <p>Research, paragraph 1: Describe your research approach and who took part.</p>
      {ul(['Method 1: An interview, survey or observation you ran.', 'Method 2: Another source of evidence.', 'Method 3: Another source of evidence.'])}
      <p>Research, paragraph 2: State the main finding and the number that supports it.</p>
      {figs('one', '16/9', ['Caption: Describe what this research image shows and why it matters.'])}
      <div class="sub">
        <h3>Second finding: a headline for the next thing you learned.</h3>
        <p>Finding, paragraph 1: Explain what you learned and how it changed the direction of the project.</p>
        <p>Finding, paragraph 2: Add the detail that makes the finding believable.</p>
        {figs('two', '4/3', ['Caption: What this image shows.', 'Caption: What this image shows.'])}
      </div>
    </section>'''
    design = f'''<section>
      <p class="eyebrow">Design</p>
      <h2>Design headline: the main decision you made and the reason for it.</h2>
      <p>Design, paragraph 1: Describe how you went from findings to ideas, such as sketches, flows or wireframes.</p>
      <p>Design, paragraph 2: Describe the trade-offs you weighed and how you chose.</p>
      {figs('two', '4/3', ['Caption: Describe this design artifact and what it shows.', 'Caption: Describe this design artifact and what it shows.'])}
    </section>'''
    validation = f'''<section>
      <p class="eyebrow">Validation</p>
      <h2>Testing headline: how you checked the design with real people.</h2>
      <p>Testing, paragraph 1: Describe the test: who took part, what they did and how many sessions you ran.</p>
      {ul(['Question 1: What you wanted to find out.', 'Question 2: What you wanted to find out.'])}
      {figs('two', '4/3', ['Caption: Describe this test photo or screenshot.', 'Caption: Describe this test photo or screenshot.'])}
    </section>'''
    solution = f'''<section>
      <p class="eyebrow">The solution</p>
      <h2>Solution headline: what you delivered and the experience it created for users.</h2>
      <p>Solution, paragraph 1: Summarize the final design and the experience users now have.</p>
      {ul(['Improvement 1: One part of the experience that changed.', 'Improvement 2: One part of the experience that changed.', 'Improvement 3: One part of the experience that changed.'])}
      <p>Solution, paragraph 2: Say what these changes delivered, with a number if you have one.</p>
      {figs('two', '4/3', ['Caption: The final design, part 1.', 'Caption: The final design, part 2.'])}
      <div class="sub">
        <h3>Feature headline: one part of the solution, in a sentence.</h3>
        <p>Feature, paragraph 1: Explain what you designed and why it helps users.</p>
        {ul(['Detail 1: What the feature does.', 'Detail 2: What the feature does.'])}
        {figs('two', '1/1', ['Caption: The feature in use.', 'Caption: The feature in use.'])}
      </div>
      <div class="sub">
        <h3>Second feature headline: another part of the solution.</h3>
        <p>Feature, paragraph 2: Explain what changed and how people responded.</p>
        {figs('one', '16/9', ['Caption: A wide view, such as a flow, a diagram or a before and after.'])}
      </div>
      <div class="sub">
        <h3 class="label center">By implementing these changes…</h3>
        {figs('three', '3/4', ['Outcome 1: What changed for users, in one line.', 'Outcome 2: What changed for users, in one line.', 'Outcome 3: What changed for users, in one line.'])}
        <p class="closing">Closing statement: one line that sums up the impact of the project.</p>
      </div>
    </section>'''
    today = f'''<section>
      <p class="eyebrow">Results</p>
      <h2>Results headline: where the project stands today and what it achieved.</h2>
      <p>Results lead-in: As of [month and year], the project has…</p>
      {ul(['Result 1: A measurable outcome.', 'Result 2: A measurable outcome.', 'Result 3: A measurable outcome.'])}
      <p><strong>Closing sentence: what this work makes possible next.</strong></p>
    </section>'''
    take = lambda k: f'<div class="goal"><h3>Takeaway {k}</h3><p>Takeaway {k} description: A lesson you learned, in one or two sentences.</p></div>'
    final = f'''<section>
      <p class="eyebrow">Final thoughts</p>
      <h2>Reflection headline: what the project taught you.</h2>
      <p>Reflection, paragraph 1: Describe the overall impact and what you are proudest of.</p>
      <p>Reflection, paragraph 2: Describe what you would do differently or what you would test next.</p>
      <h3 class="label">My takeaways:</h3>
      <div class="goals">{''.join(take(k) for k in range(1, 4))}</div>
    </section>'''
    body = '\n    '.join([hero, glance, role, results, note, problem, goals, discovery, design, validation, solution, today, final])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Valentina Luzardo</title>
  <meta name="description" content="Case study: {title}, by Valentina Luzardo.">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="case.css">
</head>
<body>
  <a class="skip" href="#main">Skip to main content</a>

  <div class="page-top">
    <a class="btn" id="back" href="index.html">← Back</a>
  </div>

  <main id="main">
    <!-- EDITABLE:START (managed by the page editor; do not rename these markers) -->
    <article class="case-body">
    {body}
    </article>
    <!-- EDITABLE:END -->

    <!-- ALSO:START (filled automatically from the Home page card) -->
    <!-- ALSO:END -->
  </main>

  <script>
    // If the visitor came from the Home page, "Back" uses the browser's history,
    // so the browser's back arrow and this button always behave the same way.
    document.getElementById('back').addEventListener('click', function (e) {{
      try {{
        if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) {{
          e.preventDefault();
          history.back();
        }}
      }} catch (err) {{ /* falls back to the normal link */ }}
    }});
  </script>
</body>
</html>
'''

open(R + 'project-1.html', 'w').write(page('Bocabox Meal Prep Website', 'Mobile', 'Website',
    'Key result sentence: the headline outcome of this project, with its number.', 'Mobile, Website', 'Month Year to Month Year', 'Your role, and who you worked with', 'project-2.html'))
open(R + 'project-2.html', 'w').write(page('Postpartum Support Service', 'In-person', 'Healthcare',
    'Key result sentence: the headline outcome of this project, with its number.', 'In-person, Healthcare', 'Month Year to Month Year', 'Your role, and who you worked with', 'project-1.html'))
print('pages written')
