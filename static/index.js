const colors = ["#ffdef2", "#f2e2ff", "#e2eeff", "#ddfffc", "#ffffe3"]
const responseContainer = document.getElementById("response-container");
const responseTitle = document.getElementById("response-title");
const responseContent = document.getElementById("response-content");

document.addEventListener("DOMContentLoaded", async () => {
	const response = await fetch("/api_endpoints");
	const data = await response.json();
	console.log(data);
	const endpoints = data;

	const endpointsContainer = document.getElementById("endpoints");

	const generateEndpoint = (endpoint, index) => {
		const endpointItem = document.createElement("div");
		endpointItem.className = "endpoint";
		const endpointElement = document.createElement("form");
		endpointElement.className = "endpoint-form";
		endpointElement.style.backgroundColor = colors[index % colors.length];
		const endpointTitleContainer = document.createElement("div");
		endpointTitleContainer.className = "endpoint-title-container";	
		const endpointTitle = document.createElement("h4");
		endpointTitle.className = "endpoint-title";
		endpointTitle.textContent = `${endpoint.path.split("/").pop().replaceAll('_', ' ').replaceAll(/\b\w/g, char => char.toUpperCase())}`;
		endpointTitleContainer.appendChild(endpointTitle);
		endpointElement.appendChild(endpointTitleContainer);
		// Create form for parameters if they exist
		if (endpoint.parameters && endpoint.parameters.length > 0) {

			endpoint.parameters.forEach(param => {
				const inputGroup = document.createElement("div");
				inputGroup.className = "input-group";

				const label = document.createElement("label");
				label.textContent = `${param.name}${param.required ? ' *' : ''}:`;
				
				const input = document.createElement("input");
				input.type = "text";
				input.name = param.name;
				input.value = param.default !== "N/A" ? param.default : "";
				input.required = param.required;

				inputGroup.appendChild(label);
				inputGroup.appendChild(input);
				endpointElement.appendChild(inputGroup);
			});
		}
		const submitContainer = document.createElement("div");
		submitContainer.className = "submit-container";
		const submitBtn = document.createElement("button");
		submitBtn.type = "submit";
		submitBtn.textContent = "Try it out";
		const body = Object.fromEntries(new FormData(endpointElement))
		console.log(body);
		submitBtn.addEventListener("click", async (e) => {
			e.preventDefault();
			try {
				const myHeaders = new Headers();
				myHeaders.append("Content-Type", "application/json");

				const response = await fetch(endpoint.path, {
					method: "POST",
					headers: myHeaders,
					body: JSON.stringify(body),
					redirect: "follow"
				});
				const data = await response.text();
				console.log(data);
				const json = JSON.parse(data);
				responseTitle.textContent = endpoint.path.split("/").pop().replaceAll('_', ' ').replaceAll(/\b\w/g, char => char.toUpperCase());
				responseContent.textContent = typeof json.result === 'object' ? JSON.stringify(json.result) : json.result;
			} catch (error) {
				console.error(error);
			}
		});
		submitContainer.appendChild(submitBtn);
		endpointElement.appendChild(submitContainer);
		endpointItem.appendChild(endpointElement);
		return endpointItem
	}
	endpoints.forEach((endpoint, index) => {
		const endpointItem = generateEndpoint(endpoint, index)
		
		// Add to container
		endpointsContainer.appendChild(endpointItem);
	});
});