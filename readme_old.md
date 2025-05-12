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