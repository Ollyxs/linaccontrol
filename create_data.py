import requests
import getpass

BASE_URL = "http://localhost:8000/api/v1"


def login(username, password):
    url = f"{BASE_URL}/auth/login"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json()


def create_linac(name, location, is_active, headers):
    url = f"{BASE_URL}/linacs/create"
    data = {"name": name, "location": location, "is_active": is_active}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_frequency(name, headers):
    url = f"{BASE_URL}/frequencies"
    data = {"name": name}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_test_category(name, headers):
    url = f"{BASE_URL}/test_categories"
    data = {"name": name}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_test(test_name, description, category_uid, headers):
    url = f"{BASE_URL}/tests/create"
    data = {
        "test_name": test_name,
        "description": description,
        "category_uid": category_uid,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_test_suite(name, test_type, test_uids, headers):
    url = f"{BASE_URL}/test_suites"
    data = {
        "test_suite_data": {"name": name, "test_type": test_type},
        "test_suite_tests_data": {"test_uid": test_uids},
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


# def create_test_suite_tests(test_suite_uid, test_uids, headers):
#     url = f"{BASE_URL}/test_suite_tests"
#     data = {"test_suite_uid": test_suite_uid, "test_uids": test_uids}
#     response = requests.post(url, json=data, headers=headers)
#     return response.json()


def create_linac_test_suite(linac_uid, test_suite_uid, frequency_uid, headers):
    url = f"{BASE_URL}/test_suites/assing"
    data = {
        "linac_uid": linac_uid,
        "test_suite_uid": test_suite_uid,
        "frequency_uid": frequency_uid,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


if __name__ == "__main__":
    # Get admin credentials
    admin_username = input("Enter admin username: ")
    admin_password = getpass.getpass("Enter admin password: ")

    # Login an admin
    login_response = login(admin_username, admin_password)
    access_token = login_response["access_token"]
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
    }

    # Create Linacs
    linac1 = create_linac("Trilogy N°4887", "San Rafael", True, headers)
    linac2 = create_linac("Silhouette N°754", "San Rafael", True, headers)

    # Create Frequencies
    frequency_daily = create_frequency("diario", headers)
    frequency_monthly = create_frequency("mensual", headers)
    frequency_yearly = create_frequency("anual", headers)

    # Create Test Category
    test_category1 = create_test_category("Mecánicos", headers)
    test_category2 = create_test_category("Seguridad", headers)
    test_category3 = create_test_category("Sistema de Parada de Emergencia", headers)
    test_category4 = create_test_category("Dosimétricos", headers)

    # Create Tests
    test1 = create_test(
        "Eje de rotación del colimador - Tolerancia 2mm",
        "",
        test_category1["uid"],
        headers,
    )
    test2 = create_test(
        "Telémetro - Tolerancia 2mm (isocentro)", "", test_category1["uid"], headers
    )
    test3 = create_test(
        "Lásers - Tolerancia 2mm (isocentro)", "", test_category1["uid"], headers
    )
    test4 = create_test("Patron Estrella MLC", "", test_category1["uid"], headers)
    test5 = create_test(
        "Valor medido de campo 50x50mm", "", test_category1["uid"], headers
    )
    test6 = create_test(
        "Valor medido de campo 100x100mm", "", test_category1["uid"], headers
    )
    test7 = create_test(
        "Valor medido de campo 200x200mm", "", test_category1["uid"], headers
    )
    test8 = create_test(
        "Enclavamientos mostrados de Monitor", "", test_category2["uid"], headers
    )
    test9 = create_test(
        "Luces en Puerta - Funcionando", "", test_category2["uid"], headers
    )
    test10 = create_test(
        "Indicador sonoro de radiación - Funcionando",
        "",
        test_category2["uid"],
        headers,
    )
    test11 = create_test(
        "Visualización por Monitor de TV", "", test_category2["uid"], headers
    )
    test12 = create_test("Interrupción por UM*", "", test_category2["uid"], headers)
    test13 = create_test(
        "Interlocks por colisión MVD-KVD-KVS (*)", "", test_category2["uid"], headers
    )
    test14 = create_test("Puerta - Funcionando", "", test_category3["uid"], headers)
    test15 = create_test("Consola - Funcionando", "", test_category3["uid"], headers)
    test16 = create_test("X-6", "", test_category4["uid"], headers)
    test17 = create_test("X-10", "", test_category4["uid"], headers)
    test18 = create_test("X-6SRS", "", test_category4["uid"], headers)
    test19 = create_test("E-6", "", test_category4["uid"], headers)
    test20 = create_test("E-9", "", test_category4["uid"], headers)
    test21 = create_test("E-12", "", test_category4["uid"], headers)
    test22 = create_test("E-16", "", test_category4["uid"], headers)
    test23 = create_test(
        "Verificación de enclavamientos y accesorios de tratamientos - Funcionando",
        "",
        test_category2["uid"],
        headers,
    )
    test24 = create_test(
        "Fijación de movimientos de camilla - Funcionando",
        "",
        test_category2["uid"],
        headers,
    )
    test25 = create_test(
        "Pulsadores de corte de energía electrica - Funcionando",
        "",
        test_category2["uid"],
        headers,
    )
    test26 = create_test(
        "Isocentro mecánico - Tolerancia 2mm", "", test_category1["uid"], headers
    )
    test27 = create_test(
        "Indicadores angulares del brazo - Tolerancia 1°",
        "",
        test_category1["uid"],
        headers,
    )
    test28 = create_test(
        "Indicadores angulares de la mesa - Tolerancia 1°",
        "",
        test_category1["uid"],
        headers,
    )
    test29 = create_test(
        "Telémetro en isocentro y linealidad - Tolerancia 2mm",
        "",
        test_category1["uid"],
        headers,
    )
    test30 = create_test("Láseres - Tolerancia 2mm", "", test_category1["uid"], headers)
    test31 = create_test(
        "Rotación del colimador - Tolerancia 2mm", "", test_category1["uid"], headers
    )
    test32 = create_test(
        "Tamaños de campo simetría, paralelismo y ortogonalidad - Tolerancia 2mm",
        "",
        test_category1["uid"],
        headers,
    )
    test33 = create_test(
        "Coincidencia de campos de luz y radiación (Placa) - Tolerancia 3mm",
        "",
        test_category1["uid"],
        headers,
    )
    test34 = create_test(
        "Horizontalidad y verticalidad de la camilla - Tolerancia 2mm",
        "",
        test_category1["uid"],
        headers,
    )
    test35 = create_test(
        "Verticalidad del eje luminoso - Tolerancia 2mm",
        "",
        test_category1["uid"],
        headers,
    )
    test36 = create_test(
        "Eje de rotación del Pedestral - Tolerancia 1mm",
        "",
        test_category1["uid"],
        headers,
    )
    test37 = create_test(
        "Test Picket Fence - Tolerancia 2mm", "", test_category1["uid"], headers
    )
    test38 = create_test(
        "Velocidad de lamina - Tolerancia 0,5 cm/s", "", test_category1["uid"], headers
    )
    test39 = create_test(
        "Test de ventana deslizante - Tolerancia 0,35 cm",
        "",
        test_category1["uid"],
        headers,
    )
    test40 = create_test(
        "Tamaños de campo de MLC - Tolerancia 2mm", "", test_category1["uid"], headers
    )

    # Create Test Suites
    test_suite_daily = create_test_suite(
        "Test diario",
        "diario",
        [
            test1["uid"],
            test2["uid"],
            test3["uid"],
            test4["uid"],
            test5["uid"],
            test6["uid"],
            test7["uid"],
            test8["uid"],
            test9["uid"],
            test10["uid"],
            test11["uid"],
            test12["uid"],
            test13["uid"],
            test14["uid"],
            test15["uid"],
            test16["uid"],
            test17["uid"],
            test18["uid"],
            test19["uid"],
            test20["uid"],
            test21["uid"],
            test22["uid"],
        ],
        headers,
    )

    test_suite_monthly = create_test_suite(
        "Test mensual",
        "mensual",
        [
            test23["uid"],
            test24["uid"],
            test25["uid"],
            test26["uid"],
            test27["uid"],
            test28["uid"],
            test29["uid"],
            test30["uid"],
            test31["uid"],
            test32["uid"],
            test33["uid"],
            test34["uid"],
            test35["uid"],
            test36["uid"],
            test37["uid"],
            test38["uid"],
            test39["uid"],
            test40["uid"],
        ],
        headers,
    )

    # Relate Linacs with Test Suites
    create_linac_test_suite(
        linac1["uid"], test_suite_daily["uid"], frequency_daily["uid"], headers
    )
    create_linac_test_suite(
        linac1["uid"], test_suite_monthly["uid"], frequency_monthly["uid"], headers
    )
    create_linac_test_suite(
        linac2["uid"], test_suite_daily["uid"], frequency_daily["uid"], headers
    )
    create_linac_test_suite(
        linac2["uid"], test_suite_monthly["uid"], frequency_monthly["uid"], headers
    )
