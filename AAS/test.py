import datetime
from pathlib import Path  # 보조 파일의 로컬 경로를 보다 쉽게 ​​처리하는 데 사용됩니다.

import pyecma376_2  # The base library for Open Packaging Specifications. We will use the OPCCoreProperties class.
from basyx.aas import model
from basyx.aas.adapter import aasx

# step 1: File 객체를 사용하여 SupplementaryFileContainer 및 AAS 및 하위 모델 설정
# step 2: AASX 패키지에 AAS 개체 및 보조 파일 쓰기
# step 3: AASX 패키지에서 AAS 개체 및 보조 파일 읽기


########################################################################################
# Step 1: File 객체를 사용하여 SupplementaryFileContainer 및 AAS 및 하위 모델 설정 #
########################################################################################

# 먼저 간단한 하위 모델을 사용하여 기본 자산 관리 셸을 만들어 보겠습니다.
# 자세한 내용은 `tutorial_create_simple_aas.py`를 참조하세요.

submodel = model.Submodel(
    id_='https://acplt.org/Simple_Submodel'
)
aas = model.AssetAdministrationShell(
    id_='https://acplt.org/Simple_AAS',
    asset_information=model.AssetInformation(
        asset_kind=model.AssetKind.INSTANCE,
        global_asset_id='http://acplt.org/Simple_Asset'
    ),
    submodel={model.ModelReference.from_referable(submodel)}
)

# AAS와 관련되지 않은 또 다른 하위 모델:
unrelated_submodel = model.Submodel(
    id_='https://acplt.org/Unrelated_Submodel'
)

# ID로 쉽게 검색할 수 있도록 이러한 객체를 ObjectStore에 추가합니다.
# 자세한 내용은 `tutorial_storage.py`를 참조하세요. 여기서는 데이터베이스 지원 ObjectStore를 사용할 수도 있습니다.
# (see `tutorial_backend_couchdb.py`).
object_store = model.DictObjectStore([submodel, aas, unrelated_submodel])


# AASX 패키지에 최종적으로 추가될 보조 파일을 보관하려면 SupplementalFileContainer가 필요합니다.
# `DictSupplementalFileContainer`는 파일 내용을 메모리의 단순 바이트 객체에 저장하는 간단한 보충파일 컨테이너입니다.
file_store = aasx.DictSupplementaryFileContainer()

# 이제 로컬 파일 시스템의 예제 파일을 보충파일컨테이너에 추가합니다.
# 이 목적을 위해서는 보충파일컨테이너에 파일 이름을 지정해야 합니다. 
# 이 이름은 컨테이너의 파일을 참조하는 데 사용되며 나중에 AASX 패키지 파일에서 파일 이름으로 사용됩니다. 
# 따라서 이 파일은 슬래시로 시작해야 하며 `/aasx/`로 시작해야 합니다. 여기서는 `/aasx/suppl/MyExampleFile.pdf`를 사용합니다.
# ComponentFileContainer의 add_file() 메소드는 내용이 다르지만 동일한 이름의 파일이 존재하는 경우 접미사를 추가하여 이름의 고유성을 보장합니다.
# 최종 이름이 반환됩니다. 또한 나중에 AASX 패키지의 메타데이터에 사용되는 파일의 MIME 유형을 지정해야 합니다. 
# (이것은 실제로 패키지 내 모든 단일 파일의 MIME 유형("콘텐츠 유형") 사양을 적용하는 기본 개방형 패키징 규칙(ECMA376-2) 형식의 요구 사항입니다.

with open(Path(__file__).parent / 'data' / 'TestFile.pdf', 'rb') as f:
    actual_file_name = file_store.add_file("/aasx/suppl/MyExampleFile.pdf", f, "application/pdf")