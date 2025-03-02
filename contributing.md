# Contributing

## How to add your organization or university

In order to add your university, you need to edit the code that this website is stored on. You can do this by cloning the repository locally, or by using the GitHub online GUI.

1. Create a file named after your institution.

    For instance, `touch universities/the-unseen-university.md` will create a file in `universities/` for your university. Then, you can add in the text that you want in that file. Look at the other files to see the expected Markdown formatting.

    Right now, you can create these in `organizations/` or `universities/`

2. Add your institution to the Table of Contents.

    You need to add it in _toc.yml. For instance, to add the Unseen University, I might add it here:

    ```yml
    chapters:
    - file: about
    - file: universities
      sections:
      ...
      - file: universities/saint-louis-university.md
      # Ingore this comment - just pointing out the new file in the line below
      - file: universities/the-unseen-university.md
      - file: universities/university-of-california-santa-cruz.md
      - file: universities/university-of-vermont.md
      - file: universities/university-of-wisconsin-madison.md
    ```

    Remember to do this alphabetically.

3. Add your institution to the relevant page.

    There's an `organizations.md` and a `universities.md` file in the main directory, and in that there is also a list of institutions. Add it there, following the style of the others. Remember to alphabetize.

4. Build.

    You need to run a build. Running `$ ./build.sh` should work, locally. If it doesn't, [open an issue](https://github.com/sustainers/academic-map/issues/new) and log that. If you're adding your text online, don't worry about running a build - the merger will be responsible for that.

5. Lint the markdown.

    If possible, run [`markdownlint`](https://github.com/igorshubovych/markdownlint-cli) on your new markdown files. This requires that you have it installed, which requires having Node installed. If that's too much to ask, just ask Richard to fun this for you.

6. Commit your results and open a Pull Request.

    If you have any questions, ping @RichardLitt wherever he is found.

    Thanks!

## Editorial notes

* "open source" should always be spelled in full, instead of "open-source" with a hyphen.
