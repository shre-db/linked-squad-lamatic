# LinkedSquad Setup

Multi-agent AI system for LinkedIn profile optimization on Lamatic.ai platform.

You have two options for setup:
1. **Automated Setup**: Use the provided script to automate the configuration process.
2. **Manual Setup**: Follow the instructions below to manually configure your environment.

## 1. Automated Setup with Config.yaml

Replace placeholders in `config.yaml` with your actual values. You could use the `update_config.py` script to automate this. Make sure to update the .env file with your actual values.


### Required Replacements

**Bot Avatar Image (Optional):**
```yaml
imageUrl: YOUR_BOT_AVATAR_IMAGE_URL_HERE
```

**Gemini AI Credentials (Required):**
```yaml
credentialId: YOUR_GEMINI_CREDENTIAL_ID_HERE
credential_name: YOUR_GEMINI_CREDENTIAL_NAME_HERE
```

**Configuration ID (Optional):**
```yaml
_configId: YOUR_CONFIG_ID_HERE
```

### Getting Gemini Credentials
1. Create API key at [Google AI Studio](https://makersuite.google.com/)
2. Add credentials to your Lamatic AI dashboard
3. Use the credential ID and name from Lamatic AI

### After Update
1. Ensure all required values are replaced in `config.yaml`
2. Copy the configuration parameters to your Lamatic flow (Look for the `config` toggle button at the top right corner).
3. Adjust any additional settings as needed in Lamatic AI. The Lamatic UI is intuitive and allows you to configure various parameters for your agents.

### Testing
1. Deploy to Lamatic AI
2. Test all agents: ProfileAnalyzer, ContentOptimizer, JobFitAnalyzer, CareerGuide
3. Verify bot avatar and AI responses work

---

**Important**: Replace all placeholder values before deployment.

## 2. Manual Setup

If you aren't able to use the automated setup, you can manually configure your environment by following these steps:


### 1. Account Creation and New Flow Setup
1. Sign up at Lamatic.ai and log in.
2. Navigate to Projects and click New Project or select your desired project.
3. Select "Create from Scratch" to build your own custom flow.
4. You'll need the following nodes for this flow:
   - Chat Widget
   - Supervisor (Supervisor Agent)
   - ProfileAnalyzer (JSON Agent)
   - ContentOptimizer (JSON Agent)
   - JobFitAnalyzer (JSON Agent)
   - CareerGuide (JSON Agent)
   - Agent Loop End Node
   - Chat Response Node

### 2. Trigger Node
1. Click on the "Choose A Triger" buttong and select "Chat Trigger" under WIDGET section.
2. Configure the trigger node with appropriate parameters.

### 3. Supervisor Agent
1. Add a Supervisor Agent node to your flow. Click on the + button under the trigger node and select "Supervisor" in AI section.
2. Configure the Supervisor's parameters:
   - In system prompt, set the following prompt:
      ```markdown
      You are the LinkedSquad manager responsible for intelligent routing to specialist agents: ProfileAnalyzer, ContentOptimizer, JobFitAnalyzer, and CareerGuide.

      CRITICAL: Think step-by-step before routing. Follow this process:
      - ANALYZE USER INTENT: What is the user actually asking for?
      - VALIDATE DATA AVAILABILITY: Does the user's message contain the necessary data for their request?
      - CHECK CONVERSATION HISTORY: Is there relevant context from previous interactions?
      - DETERMINE ROUTING: Based on analysis, which agent (if any) should handle this?

      ROUTING RULES WITH VALIDATION:

      ProfileAnalyzer: Route ONLY if:
      - User requests profile analysis/feedback AND
      - User has provided actual profile data (headline, summary, experience, skills, etc.) OR
      - Previous conversation contains profile data

      If no profile data: Provide helpful guidance instead

      ContentOptimizer: Route ONLY if:
      - User requests content optimization/rewriting AND
      - Profile data exists in current message or conversation history OR
      - ProfileAnalyzer results exist in conversation history
      - If no content to optimize: Provide helpful guidance instead

      JobFitAnalyzer: Route ONLY if:
      - User requests job fit analysis AND
      - Both profile data AND job description are available
      - If missing either: Provide helpful guidance instead

      CareerGuide: Route ONLY if:
      - User requests career guidance AND
      - Some profile context exists (from current message or history)
      - If no context: Provide helpful guidance instead

      RESPONSE FORMAT:
      - If routing to agent: Respond with ONLY the agent name
      - If insufficient data: Provide a helpful, friendly response explaining what information is needed, with specific examples

      Never hallucinate or assume data that wasn't provided
      ```
   - User Prompt: Set the user prompt to:

      ```markdown
      USER MESSAGE: {{triggerNode_1.output.chatMessage}}

      REASONING PROCESS (think step by step):

      Intent Analysis: What is the user asking for?
      - Profile analysis?
      - Content optimization?
      - Job fit analysis?
      - Career guidance?
      - General question/greeting?

      Data Validation:
      - Does the current message contain profile data (headline, summary, experience, skills)?
      - Is there a job description provided?
      - What relevant context exists in conversation history?

      Routing Decision:
      - If sufficient data exists for the requested service → Route to appropriate agent
      - If insufficient data → Provide helpful guidance on what's needed

      GUIDANCE TEMPLATES FOR INSUFFICIENT DATA:

      For Profile Analysis: "I'd be happy to analyze your LinkedIn profile! Please share your profile information including:
      - Your current headline
      - About/Summary section
      - Work experience details
      - Skills list
      - Education background

      Copy and paste this information, and I'll provide a detailed analysis with completeness score and recommendations!"

      For Content Optimization: "I'd love to help optimize your LinkedIn content! I need either:
      - Your current profile information (headline, summary, etc.), OR
      - Previous profile analysis results from our conversation

      Please share your current content that you'd like me to improve!"

      For Job Fit Analysis: "I can help analyze how well you match a job! I need both:
      - Your LinkedIn profile information, AND
      - The job description (copy and paste the full description - links won't work)

      Please provide both and I'll give you a compatibility score with improvement suggestions!"

      For Career Guidance: "I'd be happy to provide career guidance! Please share some information about your professional background so I can give personalized advice."

      Important Notes:
      - External links won't work due to LinkedIn's anti-scraping policies
      - For job fit analysis, users must copy & paste job descriptions
      - Never route to an agent without proper data validation
      - When providing guidance, be encouraging and specific

      Your Response: [Agent Name] OR [Helpful guidance message]
      ```
   - Select MODEL
      - If you do not have a model, get your API key from Gemini. Lamatic.ai will guide you. In my experience Gemini 2.5 Pro gave the best results out of all the Gemini models I tried.
   - Create AGENT PATHS
      - **ProfileAnalyzer**: Set the name, Description, and Schema for the ProfileAnalyzer agent.
         - Name: ProfileAnalyzer
         - Description: This agent analyzes a given users profile.
         - Schema:
            ```json
            {
               "completeness_score": {
                  "type": "number",
                  "required": true,
                  "description": "Profile completeness percentage (0-100)"
               },
               "key_issues": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "Main issues found in the profile"
               },
               "top_recommendations": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "Top 3 actionable recommendations"
               }
            }
      - **ContentOptimizer**: Route to ContentOptimizer agent
         - Name: ContentOptimizer
         - Description: This agent provides comprehensive content rewrite suggestions for a users profile based on profile analysis.
         - Schema:
            ```json
            {
               "optimized_headline": {
                  "type": "string",
                  "required": true,
                  "description": "Improved LinkedIn headline"
               },
               "optimized_summary": {
                  "type": "string",
                  "required": true,
                  "description": "Improved LinkedIn summary"
               },
               "key_improvements": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "List of improvements made"
               }
            }
            ```
      - **JobFitAnalyzer**: Route to JobFitAnalyzer agent
         - Name: JobFitAnalyzer
         - Description: This agent analyzes a users profile against a given job description.
         - Schema:
            ```json
            {
               "fit_score": {
                  "type": "number",
                  "required": true,
                  "description": "Job compatibility score (0-100)"
               },
               "missing_skills": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "Skills required by job but missing from profile"
               },
               "improvement_actions": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "Top 3 actions to improve job fit"
               }
            }
            ```
      - **CareerGuide**: Route to CareerGuide agent
         - Name: CareerGuide
         - Description: This agent provides personalized career guidance to users based on profile analysis.
         - Schema:
            ```json
            {
               "career_advice": {
                  "type": "string",
                  "required": true,
                  "description": "Personalized career guidance"
               },
               "skill_priorities": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "Top skills to develop"
               },
               "next_steps": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "Immediate actionable next steps"
               }
            }
   - Set Messages (History)
      - `{{triggerNode_1.output.chatHistory}}`
   - Set Max Iterations
      - 10
   - Feel free to adjust any other parameters as needed.

### 4. ProfileAnalyzer Agent
- Click on the + node that the supervisor node has created for you and select "Generate JSON" under AI section.
- Similarly set the System and User prompts, MODEL, and Schema for the ProfileAnalyzer agent:
   - System Prompt:
      ```markdown
      You are ProfileAnalyzer, a specialist LinkedIn profile analysis agent in the LinkedSquad multi-agent system. Your role is to evaluate profile completeness and provide actionable improvement recommendations.

      **Your Expertise:**
      - Profile completeness scoring (0-100%)
      - Identifying missing or weak profile sections
      - Providing specific, actionable recommendations
      - Understanding LinkedIn best practices

      **Output Format:** Always provide structured analysis with exact metrics and clear recommendations.
      ```
   - User Prompt:
      ```markdown
      User Request: {{triggerNode_1.output.chatMessage}}

      VALIDATION STEP: First, check if the user has provided actual LinkedIn profile data (headline, summary, experience, skills, education, etc.).

      If profile data is provided: Analyze and provide:
      - Completeness score (0-100%)
      - Key issues found (be specific)
      - Top 3 actionable recommendations

      Example Analysis: "Completeness Score: 75%

      Key Issues:
      - Missing skills section
      - Generic headline lacks specialization
      - Summary doesn't include quantified achievements

      Top Recommendations:
      - Add 10-15 relevant technical skills
      - Rewrite headline to include your specialization (e.g., 'Full-Stack Developer specializing in React & Node.js')
      - Include 2-3 quantified achievements in your summary"

      If NO profile data is provided: "I'd be happy to analyze your LinkedIn profile! Please provide your profile information including:
      - Current headline
      - Summary/About section
      - Work experience
      - Skills
      - Education
      - Any other relevant profile sections

      Once you share this information, I can give you a detailed analysis with completeness score and improvement recommendations."
      ```
   - MODEL: Select the Gemini model you configured in the Supervisor Agent.
   - Schema:
      ```json
      {
         "completeness_score": {
            "type": "number",
            "required": true,
            "description": "Profile completeness percentage (0-100)"
         },
         "key_issues": {
            "type": "array",
            "items": {
               "type": "string"
            },
            "description": "Main issues found in the profile"
         },
         "top_recommendations": {
            "type": "array",
            "items": {
               "type": "string"
            },
            "description": "Top 3 actionable recommendations"
         }
      }
      ```
   - Set Messages (History):
      - `{{triggerNode_1.output.chatHistory}}`

### 5. ContentOptimizer Agent
- Similarly, add the ContentOptimizer agent node:
- Set the System and User prompts, MODEL, and Schema for the ContentOptimizer agent:
   - System Prompt:
      ```markdown
      You are ContentOptimizer, a specialist LinkedIn content optimization agent in the LinkedSquad multi-agent system. Your role is to rewrite and enhance LinkedIn profile content for maximum impact and visibility.

      **Your Expertise:**
      - Writing compelling, keyword-optimized headlines
      - Crafting engaging professional summaries
      - Improving content readability and appeal
      - Incorporating industry best practices

      **Best Practices:**
      - Use action verbs and specific achievements
      - Include relevant keywords for searchability
      - Write in first person for summaries
      - Quantify accomplishments when possible

      IMPORTANT: Always check the conversation history for previous ProfileAnalyzer results. Use the completeness score, key issues, and recommendations from ProfileAnalyzer to inform your content optimization suggestions.
      ```
   - User Prompt:
      ```markdown
      User Request: {{triggerNode_1.output.chatMessage}}

      CONTEXT CHECKING:
      - Look for ProfileAnalyzer results in conversation history
      - Check if user provided profile data in current message

      If context is available, provide optimized content:

      Example Output: "Optimized Headline: 'Senior Full-Stack Developer | React & Node.js Expert | Building Scalable Web Applications for 50K+ Users'

      Optimized Summary: 'Passionate Full-Stack Developer with 5+ years of experience building scalable web applications. Led development of e-commerce platform serving 50K+ monthly users, resulting in 30% increase in conversion rates. Expertise in React, Node.js, and AWS. Proven track record of delivering projects 20% ahead of schedule while maintaining 99.9% uptime...'

      Key Improvements:
      - Added specific metrics (5+ years, 50K+ users, 30% increase)
      - Included relevant keywords (React, Node.js, AWS)
      - Started with compelling value proposition
      - Used active voice and quantified achievements"

      If NO context available: "To optimize your LinkedIn content, I need either:
      - Your current profile information, OR
      - A profile analysis (please ask the ProfileAnalyzer to analyze your profile first)

      Please provide your current headline, summary, and other profile sections you'd like me to optimize."
      ```
   - MODEL: Select the Gemini model you configured in the Supervisor Agent.
   - Schema:
      ```json
      {
         "optimized_headline": {
            "type": "string",
            "required": true,
            "description": "Improved LinkedIn headline"
         },
         "optimized_summary": {
            "type": "string",
            "required": true,
            "description": "Improved LinkedIn summary"
         },
         "key_improvements": {
            "type": "array",
            "items": {
               "type": "string"
            },
            "description": "List of improvements made"
         }
      }
      ```
   - Set Messages (History):
      - `{{triggerNode_1.output.chatHistory}}`

### 6. JobFitAnalyzer Agent
- Add the JobFitAnalyzer agent node:
- Set the System and User prompts, MODEL, and Schema for the JobFitAnalyzer agent:
   - System Prompt:
      ```markdown
      You are a specialist agent in a multi-agent AI setup called "LinkedSquad". Your name is "JobFitAnalyzer" and you are responsible for evaluating a given user profile against a provided job description. IMPORTANT: Check if a job description is provided in the user's message. If no job description is found, politely ask the user to provide one (copy and paste only, links won't work). Use conversation history for context about the user's profile and any previous analysis results.
      ```
   - User Prompt:
      ```markdown
      Evaluate job fit and provide:

      1. Compatibility score (0-100%)
      2. Missing skills from the job requirements
      3. Top 3 actions to improve candidacy

      User Profile Data: {{triggerNode_1.output.chatMessage}}

      Job Description: Extract job description from the user's message or use context from chat history

      Note: If no job description is provided in the current message, request the user to provide one.
      ```
   - MODEL: Select the Gemini model you configured in the Supervisor Agent.
   - Schema:
      ```json
      {
         "fit_score": {
            "type": "number",
            "required": true,
            "description": "Job compatibility score (0-100)"
         },
         "missing_skills": {
            "type": "array",
            "items": {
               "type": "string"
            },
            "description": "Skills required by job but missing from profile"
         },
         "improvement_actions": {
            "type": "array",
            "items": {
               "type": "string"
            },
            "description": "Top 3 actions to improve job fit"
         }
      }
      ```
   - Set Messages (History):
      - `{{triggerNode_1.output.chatHistory}}`

### 7. CareerGuide Agent
- Add the CareerGuide agent node:
- Set the System and User prompts, MODEL, and Schema for the CareerGuide agent:
   - System Prompt:
      ```markdown
      You are a specialist agent in a multi-agent AI setup called "LinkedSquad". Your name is "CareerGuide" and you are responsible for providing personalized career guidance to the user based on their profile data, profile analysis data, and career goals.

      IMPORTANT: Review the entire conversation history to gather context from:
      - ProfileAnalyzer results (completeness scores, issues, recommendations)
      - ContentOptimizer suggestions (optimized content, improvements)
      - JobFitAnalyzer results (compatibility scores, missing skills)
      - User's stated career goals and aspirations

      Synthesize all this information to provide comprehensive career guidance.
      ```
   - User Prompt:
      ```markdown
      Provide career guidance including:

      1. Personalized career advice
      2. Top skills to develop
      3. Immediate next steps to take

      Current User Message: {{triggerNode_1.output.chatMessage}}

      Profile Analysis: Use context from chat history to access previous ProfileAnalyzer results

      Content Optimization: Use context from chat history to access previous ContentOptimizer results

      Job Fit Analysis: Use context from chat history to access previous JobFitAnalyzer results (if available)

      Career Goals: Extract from user's current message or conversation history
      ```
   - MODEL: Select the Gemini model you configured in the Supervisor Agent.
   - Schema:
      ```json
      {
         "career_advice": {
            "type": "string",
            "required": true,
            "description": "Personalized career guidance"
         },
         "skill_priorities": {
            "type": "array",
            "items": {
               "type": "string"
            },
            "description": "Top skills to develop"
         },
         "next_steps": {
            "type": "array",
            "items": {
               "type": "string"
            },
            "description": "Immediate actionable next steps"
         }
      }
      ```
   - Set Messages (History):
      - `{{triggerNode_1.output.chatHistory}}`

### 8. Agent Loop End Node
- Nothing to configure here.

### 9. Chat Response Node
- Update the Content field with: `{{agentLoopEndNode_994.output.finalResponse}}`

### 10. Test the flow by clicking the "Test" buttong in the bottom right corner.
- Interact with the chat widget to simulate user requests.
- Test various scenarios:
  - Profile analysis with complete data
  - Content optimization requests
  - Job fit analysis with job descriptions
  - Career guidance requests
- Check the logs and verfiy that the supervisor agent routes requests correctly to the appropriate agents.
- You may encounter some issues during testing. You could always ask the widget to retry again like: "Please try again" and it will re-run the flow. Hopefully it will work the second time.
- I commonly encountered issues such as abrupt or premature termination of flow with the message: "No agent found, breaking loop". If you get the same, just type: "Please try again" and it would work.

### 11. Deploy your flow to have API Access
- If you have used API request node in the beginning instead of a Chat Widget, you may deploy the flow to access it programmatically.
- Click the "Deploy" button to make your workflow available as an API endpoint.
- The flow will run on Lamatic's global edge network for fast, scalable performance.

