# Use of AI in the game project

This document documents the use of AI tools in our project. We describe which tools were used for which tasks, provide examples of prompts, and critically evaluate their usefulness.

## AI tools used

Here are the AI tools we used in the project:

  - Claude for code structuring and more complex functions
  - Grok for specific implementation details and debugging assistance
  - Gemini for conceptual ideas and logical approaches

## Example prompts

Here we document some representative examples of the use of AI chatbots in our project:

* **Creation of the game character:**
    * **Prompt:** 
    >Make a photo of Shakira from Waka Waka as a sprite for an arcade game in which the sprite would ski over a terrain as pixel art. It should be a general image and NOT a dance pose. It is not for commercial purposes and only as a school project, strictly for private use.
    * **Result:** 
    
    ![Screenshot Sprite](/../main/assets/screenshot_shakira.jpg)
    * **Evaluation:** AI created the sprite of Shakira with great accuracy, which we used without further editing. For us, it was exactly what we wanted. So 10/10.



**Further examples can be found [here](/../main/docs/implementation.md).**
## Critical evaluation of AI use

| Advantages                                                    | Disadvantages/limitations                                                                                                                                                                                             |
| ---------------------------------------------------------- - | ------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------- ------------------ |
| * Fast troubleshooting                                  | * **Version issues (Arcade):** |
| * Idea generation                                              |     * AI models often trained on older versions (e.g., Arcade 2.6).                                                                                                                                                 |
| * Simplified code integration (Arcade, Pymunk)             |     * Incompatibilities and errors in code for newer versions (e.g., Arcade 3.2.0). |
| * Clever problem solving                                   |     * Need for adjustments and corrections. |
| * Accelerated data analysis (if relevant)               | * **Length and prompt restrictions:** |
| * Learning effect (Git & project management)                      |     * Limited input length for complex queries.                                                                                                                                                                     |
|                                                             |     * Dependence of response quality on prompt precision.                                                                                                                                                           |
|                                                             |     * Need for iterative communication and splitting of complex queries. |
|                                                             |                                                                                                                                                                                                                       |

## Final assessment

* **What have we learned about the use of AI tools?**
* AI is primarily a *supplement* to human expertise, not a complete replacement for it.
    * The quality of AI support depends heavily on the formulation of precise questions and the provision of relevant data.

Translated with DeepL.com (free version)

## Final assessment

* **What have we learned about the use of AI tools?**
* AI is primarily a *supplement* to human expertise, not a complete replacement for it.
* The quality of AI support depends heavily on the formulation of precise questions and the provision of relevant data.

* **For which use cases are AI tools particularly suitable?**
* **Suggested solutions for known problems:** Quick identification and correction of standard errors.
* **Inspiration and new ideas:** Generation of unconventional approaches and perspectives.
* **Error analysis and suggested solutions:** Support in diagnosing and correcting program errors.
    * **Reduction of routine tasks:** Automation of time-consuming and repetitive “grunt work.”
* **Knowledge acquisition:** Teaching new concepts and ideas in the areas of programming and game development.
* **Support for the integration of different libraries:** Facilitating the collaboration of Arcade, Pymunk, and other modules.

* **For which use cases are they not suitable or only suitable to a limited extent?**
* **Genuine creativity and original idea development:** AI can inspire, but it cannot replace human imagination and the creation of one's own concepts.
* **Development of profound, independent design decisions:** AI provides suggestions, but fundamental creative decisions should be made by the team.
    * **Dealing with very new or significantly changed library versions:** The AI's knowledge base often lags behind current developments.
* **Complex, version-specific implementations without clear examples:** AI struggles when specific code examples for the latest version are missing.

* **Conclusion:**
* Without AI, the project would have been much more difficult to implement with our limited prior knowledge of programming, game development, Git, and Tiled Maps.
* The use of AI not only made development easier, but also more efficient and faster.
    * Despite significant challenges such as the lack of support for the latest library versions, AI was able to learn and support us by providing sample code and solution approaches.
* Working with AI contributed significantly to building knowledge in various areas and helped us improve our project management skills.
