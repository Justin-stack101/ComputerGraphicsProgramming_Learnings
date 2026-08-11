# Unity Hub & Unity Engine — Complete Step-by-Step Installation & Beginner Guide

This guide provides clear, step-by-step instructions for downloading, configuring, and understanding **Unity Hub** and the **Unity Editor** for your **IT2012 (Game Development)** coursework.

---

## 💡 What is Unity Hub vs Unity Engine?

- **Unity Hub**: The control dashboard where you manage your Unity account licenses, project folders, and installed Unity Editor versions.
- **Unity Engine (Editor)**: The actual 2D/3D visual game editor where you design game levels, place sprites/models, write C# scripts, and test your game.

---

## 🛠️ Step-by-Step Installation Instructions

### Step 1: Download Unity Hub
1. Open your web browser and go to: **[unity.com/download](https://unity.com/download)**
2. Click the green button: **Download for Windows** (downloads `UnityHubSetup.exe`).

### Step 2: Install Unity Hub
1. Run `UnityHubSetup.exe` from your Downloads folder.
2. Click **I Agree** ➔ Choose install location (default `C:\Program Files\Unity Hub`) ➔ Click **Install**.
3. Once completed, keep **Run Unity Hub** checked and click **Finish**.

### Step 3: Create Account & Activate Free License
1. When Unity Hub opens, click **Sign In** (top-left icon) or **Create Account**.
2. You can sign in using your Google, GitHub, or STI student email.
3. Once signed in, activate your free Personal License:
   - Click the **Gear Icon ⚙️ (Preferences)** in the top-left corner.
   - Select **Licenses** ➔ Click **Add / Agree to Personal License**.
   - Select **"Get a free Personal license"** (100% free for students/independent developers).

### Step 4: Install the Unity Editor
1. In Unity Hub, click the **Installs** tab on the left sidebar.
2. Click the blue **Install Editor** button (top-right).
3. Under the **Official Releases** tab, select **Unity 2022.3 LTS (Long Term Support)** or **Unity 6**.
4. Under **Add Modules**:
   - Check **Microsoft Visual Studio Community** (or VS Code integration).
   - Check **Documentation**.
   - Check **Windows Build Support (IL2CPP / Mono)**.
5. Click **Install** and wait for the download to complete.

### Step 5: Create Your First 2D Project
1. In Unity Hub, click the **Projects** tab on the left.
2. Click **New Project** (top-right).
3. Select **2D Core** (for 2D games like Star Catcher).
4. Give your project a name (e.g., `StarCatcher_Unity2D`).
5. Choose a folder location ➔ Click **Create Project**.

---

## 🧠 How Unity Works (Key Concepts Made Simple)

### 1. GameObjects & Components
In Pygame, we create Python classes like `Enemy` or `Player`. In Unity:
- Everything in your scene (player, enemy, camera, background, sound) is a **GameObject**.
- You give a GameObject abilities by attaching **Components**:
  - `Sprite Renderer`: Draws your 2D image/graphics.
  - `Rigidbody2D`: Adds physics, gravity, and velocity.
  - `BoxCollider2D`: Adds collision detection (like Pygame `colliderect`).
  - `C# Script`: Your custom code logic.

### 2. Pygame vs. Unity Comparison Matrix

| Feature | Pygame (Python) | Unity (C#) |
| :--- | :--- | :--- |
| **Language** | Python (`.py`) | C# (`.cs`) |
| **Game Loop** | `while running:` loop in code | Unity handles the loop automatically |
| **Setup Code** | `__init__()` | `void Start()` |
| **Frame Update** | `update(dt)` | `void Update()` |
| **Physics** | Manual math (`pos += vel * dt`) | Built-in 2D Physics Engine (`Rigidbody2D`) |
| **Editor Interface** | Text Editor / Terminal | Visual 2D/3D Scene Inspector & Drag-and-Drop |

---

## 🚀 Hands-On First Script Example (C#)

When you write code in Unity, a standard player movement script looks like this:

```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float moveSpeed = 5.0f;

    void Start()
    {
        Debug.Log("Player spawned into the Unity Scene!");
    }

    void Update()
    {
        // Reads WASD or Arrow Keys automatically
        float moveX = Input.GetAxis("Horizontal");
        float moveY = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(moveX, moveY, 0);
        transform.position += movement * moveSpeed * Time.deltaTime;
    }
}
```

Notice how `Time.deltaTime` in C# is identical to our `dt` variable in [`main_game.py`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/main_game.py#L976)!
