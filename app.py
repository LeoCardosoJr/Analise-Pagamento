import pagamentos as pag

arquivo_conf = "pagamentos/config.cfg"

pagamentos = pag.Pagamentos(arquivo_conf)
pagamentos.carregar_dados_pagamentos()
pagamentos.preparar_dados_pagamentos()
pagamentos.calcular_dados_pagamentos()
pagamentos.carregar_dados_clientes()
pagamentos.mesclar_dados_pagamentos_e_clientes()
pagamentos.enviar_dados_processados_para_redshift()
