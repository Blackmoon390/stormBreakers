const quizData = [
    {
      scenario: "Your friend gives you a thoughtful gift. What do you do?",
      options: [
        { text: "Say thanks and express how much it means to you", correct: true },
        { text: "Nod and put it aside without saying much", correct: false },
        { text: "Ask if it was expensive", correct: false }
      ]
    },
    {
      scenario: "A classmate looks upset. How do you approach them?",
      options: [
        { text: "Ignore them and walk away", correct: false },
        { text: "Gently ask if they're okay and offer to talk", correct: true },
        { text: "Tell them to stop being dramatic", correct: false }
      ]
    },
    {
      scenario: "You're invited to a small group hangout but feel nervous. What’s a good way to respond?",
      options: [
        { text: "Politely accept and ask about the plan", correct: true },
        { text: "Ignore the invite entirely", correct: false },
        { text: "Say 'I don’t like people' and decline rudely", correct: false }
      ]
    },
    {
      scenario: "A friend shares exciting news with you. How do you respond?",
      options: [
        { text: "Celebrate with them and show excitement", correct: true },
        { text: "Say 'cool' and change the subject", correct: false },
        { text: "Tell them you're not interested", correct: false }
      ]
    }
  ];
  
  let currentIndex = 0;
  
  const scenarioEl = document.getElementById("scenario");
  const optionsEl = document.getElementById("options");
  const feedbackEl = document.getElementById("feedback");
  const nextBtn = document.getElementById("next-btn");
  
  function loadQuestion() {
    feedbackEl.textContent = "";
    nextBtn.style.display = "none";
    const current = quizData[currentIndex];
    scenarioEl.textContent = current.scenario;
    optionsEl.innerHTML = "";
  
    current.options.forEach(option => {
      const btn = document.createElement("button");
      btn.className = "option btn btn-light";
      btn.textContent = option.text;
      btn.onclick = () => {
        if (option.correct) {
          feedbackEl.textContent = "Great choice! That’s a kind and thoughtful response.";
          feedbackEl.style.color = "#2e7d32";
        } else {
          feedbackEl.textContent = " Not the best option. Try to be empathetic or thoughtful.";
          feedbackEl.style.color = "#c62828";
        }
        nextBtn.style.display = "inline-block";
      };
      optionsEl.appendChild(btn);
    });
  }
  
  nextBtn.onclick = () => {
    currentIndex = (currentIndex + 1) % quizData.length;
    loadQuestion();
  };
  
  loadQuestion();