
html_header = """
<!doctype html>
<html lang="en" data-bs-theme="auto">

<head>
  <script src="/scripts/color-modes.js"></script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="chris@christham.net">
  <title>tipitaka2500.github.io</title>
  <meta name="description"
    content="The Buddhist Era 2500 Great International Council Pāḷi Tipiṭaka, Roman Script 2005 as an HTML website.">
  <link rel="canonical" href="https://tipitaka2500.github.io">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@docsearch/css@3">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  <!-- Favicons -->
  <link rel="apple-touch-icon" href="/images/logo128.png" sizes="128x128">
  <link rel="icon" href="/images/logo.png" sizes="16x16" type="image/png">
  <link rel="icon" href="/images/logo24.png" sizes="24x24" type="image/png">
  <link rel="icon" href="/images/logo48.png" sizes="48x48" type="image/png">
  <link rel="icon" href="/images/logo128.png" sizes="128x128" type="image/png">
  <link rel="icon" href="/images/logo.ico">
  <meta name="theme-color" content="#712cf9">
  <link rel="stylesheet" type="text/css" href="/css/styles.css">
  <!-- Custom styles for this template -->
  <link href="/css/sidebars.css" rel="stylesheet">
</head>

<body>
  <svg xmlns="http://www.w3.org/2000/svg" class="d-none">
    <symbol id="check2" viewBox="0 0 16 16">
      <path
        d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z" />
    </symbol>
    <symbol id="circle-half" viewBox="0 0 16 16">
      <path d="M8 15A7 7 0 1 0 8 1v14zm0 1A8 8 0 1 1 8 0a8 8 0 0 1 0 16z" />
    </symbol>
    <symbol id="moon-stars-fill" viewBox="0 0 16 16">
      <path
        d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z" />
      <path
        d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.734 1.734 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.734 1.734 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.734 1.734 0 0 0 1.097-1.097l.387-1.162zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L13.863.1z" />
    </symbol>
    <symbol id="sun-fill" viewBox="0 0 16 16">
      <path
        d="M8 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z" />
    </symbol>
  </svg>

  <div class="dropdown position-fixed bottom-0 end-0 mb-3 me-3 bd-mode-toggle">
    <button class="btn btn-bd-primary py-2 dropdown-toggle d-flex align-items-center" id="bd-theme" type="button"
      aria-expanded="false" data-bs-toggle="dropdown" aria-label="Toggle theme (auto)">
      <svg class="bi my-1 theme-icon-active" width="1em" height="1em">
        <use href="#circle-half"></use>
      </svg>
      <span class="visually-hidden" id="bd-theme-text">Toggle theme</span>
    </button>
    <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="bd-theme-text">
      <li>
        <button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="light"
          aria-pressed="false">
          <svg class="bi me-2 opacity-50" width="1em" height="1em">
            <use href="#sun-fill"></use>
          </svg>
          Light
          <svg class="bi ms-auto d-none" width="1em" height="1em">
            <use href="#check2"></use>
          </svg>
        </button>
      </li>
      <li>
        <button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="dark"
          aria-pressed="false">
          <svg class="bi me-2 opacity-50" width="1em" height="1em">
            <use href="#moon-stars-fill"></use>
          </svg>
          Dark
          <svg class="bi ms-auto d-none" width="1em" height="1em">
            <use href="#check2"></use>
          </svg>
        </button>
      </li>
      <li>
        <button type="button" class="dropdown-item d-flex align-items-center active" data-bs-theme-value="auto"
          aria-pressed="true">
          <svg class="bi me-2 opacity-50" width="1em" height="1em">
            <use href="#circle-half"></use>
          </svg>
          Auto
          <svg class="bi ms-auto d-none" width="1em" height="1em">
            <use href="#check2"></use>
          </svg>
        </button>
      </li>
    </ul>
  </div>

  <main class="d-flex flex-nowrap" >
    <div class="flex-shrink-0 p-3 overflow-scroll" style="width: 300px;">
      <a href="/" class="d-flex align-items-center pb-3 mb-3 link-body-emphasis text-decoration-none border-bottom">
        <img src="/images/logo48.png" alt="Tipitaka2500" id="logo" width="24" />
        <span class="fs-5 ms-2 fw-semibold">tipitaka2500.github.io</span>
      </a>
      <ul class="list-unstyled ps-0">
        <li class="mb-1">
          <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
            data-bs-toggle="collapse" data-bs-target="#v-collapse" aria-expanded="false">
            Vinayapiṭaka (V)
          </button>
          <div class="collapse" id="v-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li><a href="/tipitaka/1V.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Pārājikapāḷi (1V)</a></li>
              <li><a href="/tipitaka/2V.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Pācittiyapāḷi (2V)</a></li>
              <li><a href="/tipitaka/3V.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Mahāvaggapāḷi (3V)</a></li>
              <li><a href="/tipitaka/4V.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Cūḷavaggapāḷi (4V)</a></li>
              <li><a href="/tipitaka/5V.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Parivārapāḷi (5V)</a></li>
            </ul>
          </div>
        </li>
        <li class="border-top my-2"></li>
        <li class="mb-1">
          <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
            data-bs-toggle="collapse" data-bs-target="#s-collapse" aria-expanded="false">
            Suttantapiṭaka (Sutta)
          </button>
          <div class="collapse" id="s-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li class="mb-1 ms-3">
                <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                  data-bs-toggle="collapse" data-bs-target="#d-collapse" aria-expanded="false">
                  Dīghanikāya (D)
                </button>
                <div class="collapse" id="d-collapse">
                  <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                    <li><a href="/tipitaka/6D.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Sīlakkhandhavaggapāḷi</a></li>
                    <li><a href="/tipitaka/7D.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Mahāvaggapāḷi</a></li>
                    <li><a href="/tipitaka/8D.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Pāthikavaggapāḷi</a></li>
                  </ul>
                </div>
              </li>
              <li class="mb-1 ms-3">
                <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                  data-bs-toggle="collapse" data-bs-target="#m-collapse" aria-expanded="false">
                  Majjhimanikāya (M)
                </button>
                <div class="collapse" id="m-collapse">
                  <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                    <li><a href="/tipitaka/9M.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Mūlapaṇṇāsapāḷi</a></li>
                    <li><a href="/tipitaka/10M.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Majjhimapaṇṇāsapāḷi</a></li>
                    <li><a href="/tipitaka/11M.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Uparipaṇṇāsapāḷi</a></li>
                  </ul>
                </div>
              </li>
              <li class="mb-1 ms-3">
                <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                  data-bs-toggle="collapse" data-bs-target="#sy-collapse" aria-expanded="false">
                  Saṃyuttanikāya (S)
                </button>
                <div class="collapse" id="sy-collapse">
                  <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                    <li><a href="/tipitaka/12S1.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Sagāthāvaggasaṃyuttapāḷi</a></li>
                    <li><a href="/tipitaka/12S2.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Nidānavaggasaṃyuttapāḷi</a></li>
                    <li><a href="/tipitaka/13S3.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Khandhavaggasaṃyuttapāḷi</a></li>
                    <li><a href="/tipitaka/13S4.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Saḷāyatanavaggasaṃyuttapāḷi</a></li>
                    <li><a href="/tipitaka/14S5.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Mahāvaggasaṃyuttapāḷi</a></li>
                  </ul>
                </div>
              </li>
              <li class="mb-1 ms-3">
                <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                  data-bs-toggle="collapse" data-bs-target="#a-collapse" aria-expanded="false">
                  Aṅguttaranikāya (A)
                </button>
                <div class="collapse" id="a-collapse">
                  <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                    <li><a href="/tipitaka/15A1.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Ekakanipātapāḷi</a></li>
                    <li><a href="/tipitaka/15A2.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukanipātapāḷi</a></li>
                    <li><a href="/tipitaka/15A3.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikanipātapāḷi</a></li>
                    <li><a href="/tipitaka/15A4.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Catukkanipātapāḷi</a></li>
                    <li><a href="/tipitaka/16A5.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Pañcakanipātapāḷi</a></li>
                    <li><a href="/tipitaka/16A6.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Chakkanipātapāḷi</a></li>
                    <li><a href="/tipitaka/16A7.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Sattakanipātapā</a></li>
                    <li><a href="/tipitaka/17A8.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Aṭṭhakanipātapāḷi</a></li>
                    <li><a href="/tipitaka/17A9.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Navakanipātapāḷi</a></li>
                    <li><a href="/tipitaka/17A10.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dasakanipātapāḷi</a></li>
                    <li><a href="/tipitaka/17A11.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Ekādasakanipātapāḷi</a></li>
                  </ul>
                </div>
              </li>
              <li class="mb-1 ms-3">
                <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                  data-bs-toggle="collapse" data-bs-target="#k-collapse" aria-expanded="false">
                  Khuddakanikāya (Khu)
                </button>
                <div class="collapse" id="k-collapse">
                  <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                    <li><a href="/tipitaka/18Kh.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Khuddakapāṭhapāḷi</a></li>
                    <li><a href="/tipitaka/18Dh.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dhammapadapāḷi</a></li>
                    <li><a href="/tipitaka/18Ud.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Udānapāḷi</a></li>
                    <li><a href="/tipitaka/18It.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Itivuttakapāḷi</a></li>
                    <li><a href="/tipitaka/18Sn.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Suttanipātapāḷi</a></li>
                    <li><a href="/tipitaka/19Vv.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Vimānavatthupāḷi</a></li>
                    <li><a href="/tipitaka/19Pv.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Petavatthupāḷi</a></li>
                    <li><a href="/tipitaka/19Th1.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Theragāthāpāḷi</a></li>
                    <li><a href="/tipitaka/19Th2.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Therīgāthāpāḷi</a></li>
                    <li><a href="/tipitaka/20Ap1.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Therāpadānapāḷi</a></li>
                    <li><a href="/tipitaka/20Ap2.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Therīapadānapāḷi</a></li>
                    <li><a href="/tipitaka/21Bu.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Buddhavaṃsapāḷi</a></li>
                    <li><a href="/tipitaka/21Cp.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Cariyāpiṭakapāḷi</a></li>
                    <li><a href="/tipitaka/22J.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Jātakapāḷi</a></li>
                    <li><a href="/tipitaka/23J.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Jātakapāḷi</a></li>
                    <li><a href="/tipitaka/24Mn.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Mahāniddesapāḷi</a></li>
                    <li><a href="/tipitaka/25Cn.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Cūḷaniddesapāḷi</a></li>
                    <li><a href="/tipitaka/26Ps.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Paṭisambhidāmaggapāḷi</a></li>
                    <li><a href="/tipitaka/27Ne.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Nettipāḷi</a></li>
                    <li><a href="/tipitaka/27Pe.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Peṭakopadesapāḷi</a></li>
                    <li><a href="/tipitaka/28Mi.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Milindapañhapāḷi</a></li>
                  </ul>
                </div>
              </li>
            </ul>
          </div>
        </li>
        <li class="border-top my-2"></li>
        <li class="mb-1">
          <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
            data-bs-toggle="collapse" data-bs-target="#ab-collapse" aria-expanded="false">
            Abhidhammapiṭaka (Abhi)
          </button>
          <div class="collapse" id="ab-collapse">
            <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              <li><a href="/tipitaka/29Dhs.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dhammasaṅgaṇīpāḷi</a></li>
              <li><a href="/tipitaka/30Vbh.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dhammapadapāḷi</a></li>
              <li><a href="/tipitaka/31Dht.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dhātukathāpāḷi</a></li>
              <li><a href="/tipitaka/31Pu.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Puggalapaññattipāḷi</a></li>
              <li><a href="/tipitaka/32Kv.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Kathāvatthupāḷi</a></li>
              <li class="mb-1 ms-3">
                <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                  data-bs-toggle="collapse" data-bs-target="#y-collapse" aria-expanded="false">
                  Yamaka (Y)
                </button>
                <div class="collapse" id="y-collapse">
                  <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                    <li><a href="/tipitaka/33Y1.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Mūlayamakapāḷi</a></li>
                    <li><a href="/tipitaka/33Y2.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Khandhayamakapāḷi</a></li>
                    <li><a href="/tipitaka/33Y3.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Āyatanayamakapāḷi</a></li>
                    <li><a href="/tipitaka/33Y4.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dhātuyamakapāḷi</a></li>
                    <li><a href="/tipitaka/33Y5.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Saccayamakapāḷi</a></li>
                    <li><a href="/tipitaka/34Y6.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Saṅkhārayamakapāḷi</a></li>
                    <li><a href="/tipitaka/34Y7.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Anusayayamakapāḷi</a></li>
                    <li><a href="/tipitaka/34Y8.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Cittayamakapāḷi</a></li>
                    <li><a href="/tipitaka/35Y9.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dhammayamakapāḷi</a></li>
                    <li><a href="/tipitaka/35Y10.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Indriyayamakapāḷi</a></li>
                  </ul>
                </div>
              </li>
              <li class="mb-1 ms-3">
                <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                  data-bs-toggle="collapse" data-bs-target="#p-collapse" aria-expanded="false">
                  Paṭṭhāna (P)
                </button>
                <div class="collapse" id="p-collapse">
                  <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                    <li class="mb-1 ms-3" >
                      <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                        data-bs-toggle="collapse" data-bs-target="#dh-collapse" aria-expanded="false">
                        Dhammānuloma
                      </button>
                      <div class="collapse" id="dh-collapse">
                        <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                          <li><a href="/tipitaka/36P1.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/37P1.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/38P2.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/39P3.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/39P4.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikadukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/39P5.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/39P6.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukadukapaṭṭhānapāḷi</a></li>
                        </ul>
                      </div>
                    </li>
                    <li class="mb-1 ms-3">
                      <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                        data-bs-toggle="collapse" data-bs-target="#dp-collapse" aria-expanded="false">
                        Dhammapaccanīya
                      </button>
                      <div class="collapse" id="dp-collapse">
                        <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                          <li><a href="/tipitaka/40P7.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P8.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P9.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P10.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikadukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P11.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P12.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukadukapaṭṭhānapāḷi</a></li>
                        </ul>
                      </div>
                    </li>
                    <li class="mb-1 ms-3">
                      <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                        data-bs-toggle="collapse" data-bs-target="#dl-collapse" aria-expanded="false">
                        Dhammānulomapaccanīya
                      </button>
                      <div class="collapse" id="dl-collapse">
                        <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                          <li><a href="/tipitaka/40P13.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P14.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P15.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P16.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikadukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P17.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P18.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukadukapaṭṭhānapāḷi</a></li>
                        </ul>
                      </div>
                    </li>
                    <li class="mb-1 ms-3">
                      <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"
                        data-bs-toggle="collapse" data-bs-target="#dy-collapse" aria-expanded="false">
                        Dhammapaccanīyānuloma
                      </button>
                      <div class="collapse" id="dy-collapse">
                        <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                          <li><a href="/tipitaka/40P19.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P20.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P21.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P22.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikadukapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P23.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Tikatikapaṭṭhānapāḷi</a></li>
                          <li><a href="/tipitaka/40P24.html" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Dukadukapaṭṭhānapāḷi</a></li>
                        </ul>
                      </div>
                    </li>      
                  </ul>
                </div>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>

    <div class="container overflow-scroll">
"""

html_footer = """  
    </div>
  </main>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
    crossorigin="anonymous"></script>
  <script src="/scripts/sidebars.js"></script>
</body>

</html>
"""
