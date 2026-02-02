async function Consumir_api() {
  const url = "link da api."; // A constante guarda o endereço da API em uma variável
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.json();
    console.log(result);
  } catch (error) {
    console.error(error.message);
  }
}