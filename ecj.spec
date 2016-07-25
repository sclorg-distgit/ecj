%global pkg_name ecj
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Epoch: 1

%global debug_package %{nil}
%global qualifier 201209141800

Summary: Eclipse Compiler for Java
Name: %{?scl_prefix}ecj
Version: 4.2.1
Release: 8.7%{?dist}
URL: http://www.eclipse.org
License: EPL
Group: Development/Languages
Source0: http://download.eclipse.org/eclipse/downloads/drops4/R-%{version}-%{qualifier}/%{pkg_name}src-%{version}.jar
Source1: ecj.sh.in
#Patched from http://repo2.maven.org/maven2/org/eclipse/jdt/core/3.3.0-v_771/core-3.3.0-v_771.pom 
# No dependencies are needed for ecj, dependencies are for using of jdt.core which makes no sense outside of eclipse
Source2: core-3.3.0-v_771.pom
# Always generate debug info when building RPMs (Andrew Haley)
Patch0: %{pkg_name}-rpmdebuginfo.patch
Patch1: %{pkg_name}-defaultto1.5.patch
Patch2: %{pkg_name}-generatedebuginfo.patch
# build.xml fails to include a necessary .props file in the built ecj.jar
Patch3: %{pkg_name}-include-props.patch

BuildRequires: %{?scl_prefix}ant
BuildRequires: %{?scl_prefix}javapackages-tools


%description
ECJ is the Java bytecode compiler of the Eclipse Platform.  It is also known as
the JDT Core batch compiler.

%prep
%setup -q -c
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp %{SOURCE2} pom.xml

# Remove bits of JDT Core we don't want to build
rm -r org/eclipse/jdt/internal/compiler/tool
rm -r org/eclipse/jdt/internal/compiler/apt
rm -f org/eclipse/jdt/core/BuildJarIndex.java

# JDTCompilerAdapter isn't used by the batch compiler
rm -f org/eclipse/jdt/core/JDTCompilerAdapter.java
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
ant
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -a *.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
ln -s %{pkg_name}.jar eclipse-%{pkg_name}.jar
ln -s %{pkg_name}.jar jdtcore.jar
popd

# Install the ecj wrapper script
install -p -D -m0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/ecj
sed --in-place "s:@JAVADIR@:%{_javadir}:" $RPM_BUILD_ROOT%{_bindir}/ecj

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom

%add_maven_depmap -a "org.eclipse.tycho:org.eclipse.jdt.core,org.eclipse.jdt.core.compiler:ecj" JPP-%{pkg_name}.pom %{pkg_name}.jar
%{?scl:EOF}

%files
%doc about.html
%{_mavenpomdir}/JPP-%{pkg_name}.pom
%{_mavendepmapfragdir}/%{pkg_name}
%{_bindir}/%{pkg_name}
%{_javadir}/%{pkg_name}.jar
%{_javadir}/eclipse-%{pkg_name}.jar
%{_javadir}/jdtcore.jar

%changelog
* Mon Jun  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.2.1-8.7
- Disable debuginfo

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.2.1-8.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.2.1-8.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.2.1-8.4
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.2.1-8.3
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.2.1-8.2
- SCL-ize build-requires

* Thu Feb 13 2014 Michal Srb <msrb@redhat.com> - 1:4.2.1-8.1
- First maven30 software collection build

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:4.2.1-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:4.2.1-7
- Mass rebuild 2013-12-27

* Tue Apr 09 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.2.1-6
- Add depmap for org.eclipse.jdt.core.compiler:ecj
- Resolves: rhbz#951064

* Fri Apr 05 2013 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-6
- Remove gcj entry point, native subpackage, and gcj bootstrap entirely (fixes RHBZ927665).

* Wed Mar 06 2013 Karsten Hopp <karsten@redhat.com> 1:4.2.1-5
- add BR java-devel for !with_gcjbootstrap

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-3
- Patch GCCMain to avoid dummy symbols.

* Wed Oct 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.2.1-2
- Add depmap satysfying Tycho req.

* Wed Jul 31 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-1
- Update to 4.2.1 upstream version.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-13
- Add missing epoch to native subpackage requires.

* Tue Apr 17 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-12
- Separate gcj in subpackage.

* Mon Jan 16 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-11
- Patch pom file to better represent ecj and not jdt.core .
- Guidelines fixes.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.4.2-8
- Fix add_to_maven_depmap call (Resolves rhbz#655796)

* Mon Dec 21 2009 Deepak Bhole <dbhole@redhat.com> - 1:3.4.2-7
- Fix RHBZ# 490936. If CLASSPATH is not set, add . to default classpath.

* Wed Sep 9 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-6
- Add maven pom and depmaps.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-4
- Add patch to generate full debuginfo for ecj itself

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-3
- Add BR for aot-compile-rpm

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-2
- Add BR for ant

* Fri Mar 6 2009 Andrew Overholt <overholt@redhat.com> 1:3.4.2-1
- 3.4.2

* Tue Dec 9 2008 Andrew Overholt <overholt@redhat.com> 1:3.4.1-1
- 3.4.1
- Don't conditionalize building of gcj AOT bits (we're only building
  this for gcj and IcedTea bootstrapping).

* Mon Jan 22 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- Add eclipse-ecj-gcj.patch.

* Fri Jan 12 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- First version for Fedora 7.
- Add BR: java-devel for jar.

* Thu Nov 02 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.1-1jpp
- First version for JPackage.

* Mon Jul 24 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- Add versionless ecj.jar symlink in /usr/share/java.

* Wed Jul 19 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- 3.2.0.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 07 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.9
- Don't build for ppc or ia64.

* Sun Feb 20 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.6
- Upgrade back to 3.1M4.
- Don't build for i386 and x86_64.
- Provide eclipse-ecj until we can deprecate this package.

* Fri Jan 14 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.4
- build for all but x86

* Thu Jan 13 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.3
- build for ppc exclusively

* Wed Jan 12 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.2
- Add RPM_OPT_FLAGS workaround.

* Tue Jan 11 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.1
- New version.

* Mon Sep 27 2004 Gary Benson <gbenson@redhat.com> 2.1.3-5
- Rebuild with new katana.

* Fri Jul 22 2004 Gary Benson <gbenson@redhat.com> 2.1.3-4
- Build without bootstrap-ant.
- Split out lib-org-eclipse-jdt-internal-compiler.so.

* Tue Jul  6 2004 Gary Benson <gbenson@redhat.com> 2.1.3-3
- Fix ecj-devel's dependencies.

* Wed Jun  9 2004 Gary Benson <gbenson@redhat.com> 2.1.3-2
- Work around an optimiser failure somewhere in ecj or gcj (#125613).

* Fri May 28 2004 Gary Benson <gbenson@redhat.com>
- Build with katana.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com> 2.1.3-1
- Initial Red Hat Linux build.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com>
- Upgraded to latest version.

* Sun Jul 20 2003 Anthony Green <green@redhat.com>
- Add %%doc

* Fri Jul 18 2003 Anthony Green <green@redhat.com>
- Initial RHUG build.
