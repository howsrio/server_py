document.getElementById("save-button").addEventListener("click", async () => {
  const name = document.getElementById("name").value;
  const preferences = document.getElementById("preferences").value;

  if (!name || !preferences) {
    alert("이름과 취향을 모두 입력해주세요.");
    return;
  }

  const response = await fetch("/save_preferences", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `name=${encodeURIComponent(name)}&preferences=${encodeURIComponent(preferences)}`,
  });

  const result = await response.json();
  alert(result.message);
});

document.getElementById("delete-button").addEventListener("click", async () => {
  const name = document.getElementById("name").value;

  if (!name) {
    alert("삭제할 이름을 입력해주세요.");
    return;
  }

  const response = await fetch("/delete_preferences", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `name=${encodeURIComponent(name)}`,
  });

  const result = await response.json();
  alert(result.message);
});

document.getElementById("view-button").addEventListener("click", async () => {
  const response = await fetch("/view_preferences");
  const data = await response.json();

  const resultsSection = document.getElementById("results");
  const dataList = document.getElementById("data-list");
  dataList.innerHTML = ""; // 기존 데이터 초기화

  data.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = `이름: ${item.name}, 취향: ${item.preferences}`;
    dataList.appendChild(listItem);
  });

  resultsSection.style.display = "block";
});
