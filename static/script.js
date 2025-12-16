function analyzeImage() {
    var input = document.getElementById('imageInput');
    if (input.files.length === 0) {
        alert("Please select an image!");
        return;
    }

    var btn = document.querySelector("button");
    btn.innerText = "Analyzing...";
    btn.disabled = true;

    var formData = new FormData();
    formData.append('file', input.files[0]);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('result-area').style.display = 'block';
        document.getElementById('displayImage').src = data.image_url;
        document.getElementById('colorName').innerText = data.color_name;
        document.getElementById('aiMessage').innerText = data.message;
        document.getElementById('detectedColorBox').style.backgroundColor = data.dominant_color_rgb;

        
        var list = document.getElementById('paletteList');
        list.innerHTML = '';
        data.palette.forEach(color => {
            let li = document.createElement('li');
            li.className = 'palette-item';

            let hex = color.split(" ")[0]; 
            li.style.borderLeft = `20px solid ${hex}`;
            li.innerText = color;

            list.appendChild(li);
        });

        
        var fList = document.getElementById('furnitureList');
        fList.innerHTML = '';
        data.furniture.forEach(item => {
            let li = document.createElement('li');
            li.innerText = item;
            fList.appendChild(li);
        });

       
        var aList = document.getElementById('accessoryList');
        aList.innerHTML = '';
        data.accessories.forEach(item => {
            let li = document.createElement('li');
            li.innerText = item;
            aList.appendChild(li);
        });

        
        var lList = document.getElementById('lightingList');
        lList.innerHTML = '';
        data.lighting.forEach(item => {
            let li = document.createElement('li');
            li.innerText = item;
            lList.appendChild(li);
        });

    
        var wList = document.getElementById('wallList');
        wList.innerHTML = '';
        data.wall.forEach(item => {
            let li = document.createElement('li');
            li.innerText = item;
            wList.appendChild(li);
        });

        btn.innerText = "Analyze Room";
        btn.disabled = false;
    })
    .catch(err => {
        console.error(err);
        alert("Something went wrong.");
        btn.innerText = "Analyze Room";
        btn.disabled = false;
    });
}
