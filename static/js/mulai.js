const mydata = document.getElementById("mydata");
const nama_file = document.getElementById("nama_file");
const ukuran_file = document.getElementById("ukuran_file");
const kotak_deskripsi = document.getElementById("kotak_deskripsi");
const label_input = document.getElementById("label_input");
const myform = document.getElementById("myform");
const loader = document.getElementById("loader");
const kotak_informasi = document.getElementById("kotak_informasi");
const ukuran_sebelum = document.getElementById("ukuran_sebelum");
const ukuran_setelah = document.getElementById("ukuran_setelah");
const nilai_rc = document.getElementById("nilai_rc");
const nilai_cr = document.getElementById("nilai_cr");
const nilai_ss = document.getElementById("nilai_ss");
const tombol_simpan_hasil_kompresi = document.getElementById("tombol_simpan_hasil_kompresi");
const loader2 = document.getElementById("loader2");
const loader3 = document.getElementById("loader3");
const my_file = document.getElementById("my_file");
const waktu = document.getElementById("waktu");

loader.style.display = 'none';
kotak_informasi.style.display = 'none';

mydata.addEventListener('change', () => {
    const files = mydata.files;

    if (files.length > 0) {
        kotak_deskripsi.style.display = "block";
        nama_file.textContent = files[0].name;
        ukuran_file.textContent = `${(files[0].size / 1024).toFixed(2)} kb`;
        label_input.textContent = "ganti file";
    }
});

BASE_URL = "http://127.0.0.1:5000";

// myform
myform.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(myform);

    try {
        loader.style.display = 'block';
        kotak_informasi.style.display = 'none';
        const response = await axios.post(`${BASE_URL}/mulai/mulaikompresi`, formData);

        console.log("berhasil dijalankan");
        loader.style.display = 'none';
        kotak_informasi.style.display = 'block';

        // tampilkan data yang diterima
        dataku = response.data
        // console.log(JSON.stringify(response.data));
        console.log(dataku);

        ukuran_sebelum.textContent = `${dataku.informasi.ukuran_awal} kb`;
        ukuran_setelah.textContent = `${dataku.informasi.ukuran_setelah} kb`;
        nilai_rc.textContent = `${dataku.informasi.nilai_rc}`;
        nilai_cr.textContent = `${dataku.informasi.nilai_cr} %`;
        nilai_ss.textContent = `${dataku.informasi.nilai_ss} %`;
        waktu.textContent = `${dataku.informasi.waktu} s`;
        
    } catch (error) {
        kotak_informasi.style.display = 'none';
        loader.style.display = 'none';
        console.log("gagal dijalankan");
    }

})


loader2.style.display = 'none';
tombol_simpan_hasil_kompresi.addEventListener("click", async () => {

    try {
        loader2.style.display = 'block';
        const response = await axios.get(`${BASE_URL}/mulai/downloadhasilkompresi`, {
            // responseType: 'blob'
        });
        // console.log(response);

        window.open(`${BASE_URL}/mulai/downloadhasilkompresi`);

        // const url = URL.createObjectURL(response.data);
        // const a = document.createElement("a");
        // a.href = url;
        // a.download = "conth";
        // a.style.display = "none";
        // document.body.appendChild(a);
        // a.click();
        // a.remove();
        // URL.revokeObjectURL(url);

        console.log("berhasil dijalankan11");
        loader2.style.display = 'none';

        // tampilkan data yang diterima
        // dataku = response.data
        // console.log(JSON.stringify(response.data));
        // console.log(dataku);

    } catch (error) {
        loader2.style.display = 'none';
        console.log("gagal dijalankan");
    }
});

loader3.style.display = "none";
my_file.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("my_file", file);

    try {
        loader3.style.display = "block";
        console.log("sukses dekompresi");
        // const response = await axios.get(`${BASE_URL}/mulai/dekompresifile`);
        const response = await axios.post(`${BASE_URL}/mulai/dekompresifile`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        loader3.style.display = "none";
        console.log("berhasil");

        window.open(`${BASE_URL}/mulai/downloadhasildekompresi`);

    } catch (error) {
        loader3.style.display = "none";
        console.log("gagal dekompresi");
    }
});