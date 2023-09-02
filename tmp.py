from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Datos de entrenamiento: edad, salario y si compró el producto (0 = no, 1 = sí)
data = [
    (25, 50000, 0),
    (30, 60000, 1),
    (22, 45000, 0),
    (40, 70000, 1),
    (35, 80000, 1),
    (28, 55000, 0),
]

# Separar características (X) y etiquetas (y)
X = [(age, salary) for age, salary, _ in data]
y = [label for _, _, label in data]

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo de árbol de decisión
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy:.2f}")
