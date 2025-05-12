ReforgeAI is an agentic AI system that automatically analyzes existing code, 
generates a transformation plan, and completes the transformation tasks suggested by the plan. 
It identifies and updates package dependencies and refactors deprecated and inefficient code components, 
switching to new language frameworks and incorporating security best practices. 
Once complete, the transformed code can be reviewed, complete with build and test results, 
before accepting the changes.

usage 

python3 gen_docs.py temp_codebase/kitchensink/

python3 gen_modern.py 



list the requirements to compile legacy and j21 code


- read a lot about app modernization and app modernization with gen ai
- manually modernized kitchensink with the help of an llm and wrote down all rpoblems and solutions
- started with reforge ai
- first the gen_docs pipeline, it was fairly simple to reach the result even if it was a trial and error process
    - final results looks good to me
    - running multiple times produces differents results see docs_ver0_best
    - sometins some documents are empty, is openai always servige the same model? looks like after heavy usage model performaces degrades or it is a differnt and less powerfull model
- second step analyze the documents, analyze the code and produce the yaml file with the approved plan
- third step create gen modern
  - explain pieline
  - read all the documents, the agent was not reading them all it took a whole for me to understand.
    - luckly i had the monitoring pipeline in place 
      - https://app.langtrace.ai/project/cmadwbajj0007yfqm1yefsv96/traces
      - https://serper.dev/dashboard
    - Build agent powerd with llm was allucinating, simulating a maven build output!!!!
- human feedback is extremly important
  - see the feedback in gen moder tasks.xml
    - feedbackj to see if the model read all the docs
    - feedback to see if the agent did the right changes
  - in docs there shall be a feedback for each doc, not in this evr for simplicity
- guardrails for paths 
- see docs improvements.md to discuss what i would do next 
- 4.1mini was not able to make any succesfull build I had to switch to 4.1
- sometimes in gen moder it was refusing to read, i guess the llm chosen the wrong tool
  no matter what feedback i gave it was not abe to read. Restartin made it works
- gen moder, sometimes it makes sometimes it doesn't make it 
- manualy delete folder since agent does not have the capability to delete folders


https://www.mongodb.com/press/mongodb-launches-new-program-for-enterprises-to-build-modern-applications-with-advanced-generative-ai-capabilities
https://www.mongodb.com/press/mongodb-launches-new-program-for-enterprises-to-build-modern-applications-with-advanced-generative-ai-capabilities
https://mail.google.com/mail/u/0/#inbox/KtbxLvhZlHpMDPRFGCCvXslXJSVFDWNlCL?projector=1&messagePartId=0.1
https://medium.com/@jelkhoury880/leveraging-large-language-models-for-automated-code-migration-and-repository-level-tasks-part-ii-24d23c3cc7a0
https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-transformation.html
https://www.ibm.com/think/topics/generative-ai-for-application-modernization
https://www.nttdata.com/global/en/insights/focus/2025/generative-ai-a-transformative-force-in-legacy-app-modernization#:~:text=Early%20adopters%20have%20reported%20significant,risks%20associated%20with%20system%20overhauls
https://medium.com/@adnanmasood/the-unreasonable-effectiveness-of-generative-ai-in-legacy-application-modernization-0e81d294f894#:~:text=promise%20faster%20project%20timelines%2C%20lower,impact%20of%20this%20new%20paradigm
https://www.mongodb.com/resources/solutions/use-cases/application-modernization
https://medium.com/@jelkhoury880/why-general-purpose-llms-wont-modernize-your-codebase-and-what-will-eaf768481d38
https://medium.com/@AlexanderObregon/modernizing-legacy-java-applications-best-practices-and-considerations-a01b3b52ee7a
https://github.com/janus-llm/janus-llm
https://github.com/spring-projects-experimental/spring-boot-migrator
https://www.youtube.com/watch?v=jp-fBw07r7c&t=13s
https://www.ibm.com/think/topics/langchain?mhsrc=ibmsearch_a&mhq=langchain
https://www.ibm.com/think/topics/crew-ai?utm_source=chatgpt.com
https://github.com/facebookresearch/CodeGen
https://github.com/facebookresearch/TransCoder
https://martinfowler.com/articles/legacy-modernization-gen-ai.html
https://medium.com/@adnanmasood/the-unreasonable-effectiveness-of-generative-ai-in-legacy-application-modernization-0e81d294f894
https://aws.amazon.com/blogs/apn/accelerate-legacy-app-modernization-with-virtusa-and-aws-generative-ai/#:~:text=The%20Challenge%20of%20Legacy%20Systems
https://www.nttdata.com/global/en/insights/focus/2025/generative-ai-a-transformative-force-in-legacy-app-modernization
https://arxiv.org/abs/2405.04324#:~:text=and%20documenting%20code%2C%20maintaining%20repositories%2C,optimized%20for%20enterprise%20software%20development
https://arxiv.org/html/2411.14971v1#:~:text=comments%20for%20MUMPS%20and%20ALC,highlight%20the%20limitations%20of%20current
https://arxiv.org/pdf/2305.12138
https://arxiv.org/html/2306.11943v2
https://dev.to/aws-heroes/code-transformation-with-amazon-q-40df
https://www.researchgate.net/publication/390620560_Leveraging_Large_Language_Models_for_Automated_Code_Generation_Testing_and_Debugging_in_Modern_Development_Pipelines
https://arxiv.org/abs/2309.12499?s=09
https://arxiv.org/abs/2410.24119
https://github.com/janus-llm/janus-llm?tab=readme-ov-file
https://arxiv.org/html/2411.14971v1#bib.bib6
https://medium.com/@fareedkhandev/gpt-migrate-convert-your-codebase-to-any-language-framework-cc1f846e4630
https://github.com/joshpxyne/gpt-migrate
https://github.com/aws-samples/rearchitecting-modernapps-sample/tree/main
https://www.youtube.com/watch?v=kJLiOGle3Lw
https://aws.amazon.com/q/
https://github.com/konveyor/kai
https://github.com/IBM/watsonx-code-assistant
https://github.com/AgiFlow/repo-upgrade
https://agiflow.io/https://medium.com/@jelkhoury880/leveraging-large-language-models-for-automated-code-migration-and-repository-level-tasks-part-ii-24d23c3cc7a0
https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-transformation.html
https://www.ibm.com/think/topics/generative-ai-for-application-modernization
https://www.nttdata.com/global/en/insights/focus/2025/generative-ai-a-transformative-force-in-legacy-app-modernization#:~:text=Early%20adopters%20have%20reported%20significant,risks%20associated%20with%20system%20overhauls
https://medium.com/@adnanmasood/the-unreasonable-effectiveness-of-generative-ai-in-legacy-application-modernization-0e81d294f894#:~:text=promise%20faster%20project%20timelines%2C%20lower,impact%20of%20this%20new%20paradigm
https://www.mongodb.com/resources/solutions/use-cases/application-modernization
https://medium.com/@jelkhoury880/why-general-purpose-llms-wont-modernize-your-codebase-and-what-will-eaf768481d38
https://medium.com/@AlexanderObregon/modernizing-legacy-java-applications-best-practices-and-considerations-a01b3b52ee7a
https://github.com/janus-llm/janus-llm
https://github.com/spring-projects-experimental/spring-boot-migrator
https://www.youtube.com/watch?v=jp-fBw07r7c&t=13s
https://www.ibm.com/think/topics/langchain?mhsrc=ibmsearch_a&mhq=langchain
https://www.ibm.com/think/topics/crew-ai?utm_source=chatgpt.com
https://github.com/facebookresearch/CodeGen
https://github.com/facebookresearch/TransCoder
https://martinfowler.com/articles/legacy-modernization-gen-ai.html
https://medium.com/@adnanmasood/the-unreasonable-effectiveness-of-generative-ai-in-legacy-application-modernization-0e81d294f894
https://aws.amazon.com/blogs/apn/accelerate-legacy-app-modernization-with-virtusa-and-aws-generative-ai/#:~:text=The%20Challenge%20of%20Legacy%20Systems
https://www.nttdata.com/global/en/insights/focus/2025/generative-ai-a-transformative-force-in-legacy-app-modernization
https://arxiv.org/abs/2405.04324#:~:text=and%20documenting%20code%2C%20maintaining%20repositories%2C,optimized%20for%20enterprise%20software%20development
https://arxiv.org/html/2411.14971v1#:~:text=comments%20for%20MUMPS%20and%20ALC,highlight%20the%20limitations%20of%20current
https://arxiv.org/pdf/2305.12138
https://arxiv.org/html/2306.11943v2
https://dev.to/aws-heroes/code-transformation-with-amazon-q-40df
https://www.researchgate.net/publication/390620560_Leveraging_Large_Language_Models_for_Automated_Code_Generation_Testing_and_Debugging_in_Modern_Development_Pipelines
https://arxiv.org/abs/2309.12499?s=09
https://arxiv.org/abs/2410.24119
https://github.com/janus-llm/janus-llm?tab=readme-ov-file
https://arxiv.org/html/2411.14971v1#bib.bib6
https://medium.com/@fareedkhandev/gpt-migrate-convert-your-codebase-to-any-language-framework-cc1f846e4630
https://github.com/joshpxyne/gpt-migrate
https://github.com/aws-samples/rearchitecting-modernapps-sample/tree/main
https://www.youtube.com/watch?v=kJLiOGle3Lw
https://aws.amazon.com/q/
https://github.com/konveyor/kai
https://github.com/IBM/watsonx-code-assistant
https://github.com/AgiFlow/repo-upgrade
https://agiflow.io/