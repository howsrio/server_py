let selectedFriendNames = []; // 선택된 친구 이름
let friendDetails = {}; // 서버에서 가져올 친구 세부 속성

// 친구 이름 목록 불러오기
document.getElementById("add-friend-button").addEventListener("click", async function () {
  const friendList = document.getElementById("friend-list");

  try {
    const response = await fetch("/get-friends-names");
    if (!response.ok) throw new Error("서버에서 친구 이름 데이터를 가져오지 못했습니다.");

    const data = await response.json();
    const names = data.names;

    // 친구 목록 표시
    friendList.innerHTML = "";
    if (names.length === 0) {
      friendList.innerHTML = "<div>친구 목록이 비어있습니다.</div>";
    } else {
      names.forEach(name => {
        const friendItem = document.createElement("div");
        friendItem.className = "friend-item";
        friendItem.textContent = name;

        friendItem.addEventListener("click", function () {
          addFriendToSelection(name);
          friendList.style.display = "none";
        });

        friendList.appendChild(friendItem);
      });
    }
    friendList.style.display = "block";
  } catch (error) {
    console.error("친구 이름 불러오기 실패:", error);
    alert("친구 이름 목록을 불러오는 데 실패했습니다.");
  }
});

// 친구 선택 함수
function addFriendToSelection(name) {
  const selectedFriendsContainer = document.getElementById("selected-friends-container");

  if (!selectedFriendNames.includes(name)) {
    selectedFriendNames.push(name);

    const friendItem = document.createElement("span");
    friendItem.className = "selected-friend";
    friendItem.textContent = name;

    const removeButton = document.createElement("span");
    removeButton.className = "remove-friend";
    removeButton.textContent = "x";
    removeButton.addEventListener("click", function () {
      selectedFriendsContainer.removeChild(friendItem);
      selectedFriendNames = selectedFriendNames.filter(n => n !== name);
    });

    friendItem.appendChild(removeButton);
    selectedFriendsContainer.appendChild(friendItem);
  }
}

// 모임 생성 시 서버에서 세부 속성 불러오기
document.getElementById("filter-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const name = document.getElementById("meeting-name").value;
  const date = document.getElementById("meeting-date").value;
  const time = document.getElementById("meeting-time").value;

  try {
    // 서버에서 선택된 친구들의 세부 속성 가져오기
    const response = await fetch("/get-friend-details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ names: selectedFriendNames }),
    });

    if (!response.ok) throw new Error("친구 세부 데이터를 가져오는 데 실패했습니다.");
    friendDetails = await response.json();

    // 데이터 출력 (테스트용)
    console.log("모임 이름:", name);
    console.log("날짜:", date);
    console.log("시간:", time);
    console.log("선택된 친구 세부 정보:", friendDetails);

    alert("모임이 성공적으로 생성되었습니다!");
  } catch (error) {
    console.error("모임 생성 실패:", error);
    alert("모임 생성 중 오류가 발생했습니다.");
  }
});
