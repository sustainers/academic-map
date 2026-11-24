# Contributing

Anyone is welcome to contribute. Here is a small guide for adding your organization.

## How to add your organization or university

In order to add your university, you need to edit the code that this website is stored on. You can do this by cloning the repository locally, or by using the GitHub online GUI.

1. Create a file named after your institution.

    For instance, `touch universities/the-unseen-university.md` will create a file in `universities/` for your university. Then, you can add in the text that you want in that file. Look at the other files to see the expected Markdown formatting. For an organization, you can start from the template in `organizations/example.md`.

    Right now, you can create these in `universities/`, `organizations/`, `research-institutions/`, `service-providers/`, `events/`, or `funders/`.

2. Add your institution to the Table of Contents.

    You need to add it in _toc.yml. For instance, to add the Unseen University, I might add it here:

    ```yml
    chapters:
    - file: about
    - file: universities
      sections:
      ...
      - file: universities/saint-louis-university.md
      # Ignore this comment - just pointing out the new file in the line below
      - file: universities/the-unseen-university.md
      - file: universities/university-of-california-santa-cruz.md
      - file: universities/university-of-vermont.md
      - file: universities/university-of-wisconsin-madison.md
    ```

    Remember to do this alphabetically.

3. Add your institution to the index page for its folder.

    Each folder has an `index.md` that lists every entry in it: for instance, `universities/index.md` or `organizations/index.md`. Add a link to your new file there, following the style of the others. Remember to alphabetize.

    Make the link bold, like `- **[The Unseen University](./the-unseen-university.md)**`. On index pages, a bold link means the entry has its own page on this site. Links to outside websites aren't bold.

4. Add your institution to the member lists of any groups it belongs to.

    If your entry says it is a *Member of* an organization that has its own page here, add your institution to that page's member list too. For instance, if your entry lists `[CURIOSS](https://curioss.org/)`, add a link to your file in the Members section of `organizations/curioss.md`, alphabetically.

5. Build.

    You need to run a build. Running `$ ./scripts/build.sh` should work, locally. If it doesn't, [open an issue](https://github.com/CURIOSSorg/academic-map/issues/new) and log that. If you're adding your text online, don't worry about running a build - the merger will be responsible for that.

6. Run the checks.

    If possible, run `npm install` and then `npm run checks`. This lints the markdown, checks links, and makes sure your file is in `_toc.yml`, its folder's `index.md`, and any member lists it should be on. This requires having Node installed. If that's too much to ask, don't worry: the same checks run automatically on your Pull Request, or you can ask Richard to run them for you.

7. Commit your results and open a Pull Request.

    If you have any questions, ping @RichardLitt wherever he is found.

    Thanks!

## Logos and funding calls from CURIOSS

Two things on this site come from [curioss.org](https://curioss.org/) each time it builds, so they aren't edited here:

* **CURIOSS member logos.** Each member's logo appears at the top of its page. To add or change a logo, edit `data/members.yml` in the [curioss.org repository](https://github.com/CURIOSSorg/curioss.org), and set `mapPage` to the entry's path here (for instance, `universities/the-unseen-university`).
* **Open funding calls.** Funder pages list the calls that are open now, from CURIOSS's [list of funding opportunities](https://curioss.org/resources/funding-opportunities/). To list a call on a funder page here, add that page to the call's `mapPages` in `data/funding-opportunities.yml` in the curioss.org repository.

The build runs `scripts/sync_curioss.py` to fetch them, and the site rebuilds daily to pick up changes.

## Editorial notes

* "open source" should always be spelled in full, instead of "open-source" with a hyphen.
